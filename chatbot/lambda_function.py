import json
import os
import mysql.connector
import requests

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user=os.environ['user'],
            password=os.environ['password'],
            host=os.environ['host'],
            database=os.environ['database']
        )
        return conn
    except Exception as e:
        return None

class IntentClassifier:
    def __init__(self):
        # Load configurations and data
        self.intents = self._load_json('intents.json')
        self.responses = self._load_json('responses.json')
        self.queries = self._load_json('queries.json')

        # Initialize Groq client
        self.api_key = os.environ['api_key']
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"
        self.fallback_intent = "fallback"

    def _load_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def classify_intent(self, prompt):
        prompt_system = (
            "Você é um classificador de intenções. Responda APENAS com a chave da intent correspondente ou 'fallback'.\n"
            "Intenções disponíveis:\n"
        )
        for intent in self.intents:
            patterns = ", ".join(intent['patterns'])
            prompt_system += f"- {intent['response_key']}: {patterns}\n"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": f"Classifique: '{prompt}'"}
            ],
            "temperature": 0.1,
            "max_tokens": 10,
            "stop": ["\n"]
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            intent_key = data["choices"][0]["message"]["content"].strip().lower()
        except Exception as e:
            print(f"Erro ao chamar Groq API: {e}")
            intent_key = self.fallback_intent

        valid_keys = [intent['response_key'] for intent in self.intents]
        return intent_key if intent_key in valid_keys else self.fallback_intent

    def execute_sql_query(self, query_key, params=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.queries[query_key], params or ())
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def format_response(self, intent_key, data=None):
        template = self.responses.get(intent_key, "Desculpe, não entendi.")
        if not data:
            return template
        if isinstance(data, list):
            if not data:
                return "Nenhum resultado encontrado."
            header = " | ".join(data[0].keys())
            rows = "\n".join([" | ".join(map(str, row.values())) for row in data])
            return f"{template}\n\n{header}\n{rows}"
        return template.replace("{dados}", str(data))

    def respond(self, prompt):
        intent_key = self.classify_intent(prompt)
        if intent_key in self.queries:
            data = self.execute_sql_query(intent_key)
            return self.format_response(intent_key, data)
        return self.responses.get(intent_key, self.responses.get(self.fallback_intent, "Desculpe, não entendi."))

classifier = IntentClassifier()

def lambda_handler(event, context):
    try:
        if 'body' in event:
            body = json.loads(event['body'])
            prompt = body['prompt']
        else:
            prompt = event['prompt']
        if not prompt:
            return json.dumps({'error': 'O campo "prompt" é obrigatório.'}), 400

        bot_response = classifier.respond(prompt)
        return json.dumps({'response': bot_response}), 200

    except Exception as e:
        return json.dumps({'error': str(e)}), 500