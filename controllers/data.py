import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime

# Configuração do Flask
app = Flask(__name__)
api = Api(app)

# Configuração do banco de dados PostgreSQL
DB_HOST = "database-2.clhwd5ytyuym.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "postgres"
DB_NAME = "postgres"
DB_PASS = "postgres"

# Função para criar uma conexão com o banco de dados PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            connect_timeout=10  # Timeout para evitar bloqueios
        )
        print("Conexão estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

class Data(Resource):
    def get(self):
        conn = get_db_connection()
        if conn is None:
            return {"error": "Falha ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM Data")
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(results)
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        conn = get_db_connection()
        if conn is None:
            return {"error": "Falha ao conectar ao banco de dados"}, 500

        try:
            data = request.json
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "INSERT INTO Data (date_time, metal, plastic) VALUES (%s, %s, %s)",
                (time_now, data['metal'], data['plastic'])
            )
            conn.commit()

            # Recupera o registro inserido
            cursor.execute("SELECT date_time, metal, plastic FROM Data WHERE date_time = %s", (time_now,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return jsonify(result)
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(Data, '/data')

if __name__ == '__main__':
    app.run(debug=True)