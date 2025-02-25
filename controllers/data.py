from flask import request, jsonify
from flask_restful import Resource
from google.cloud import bigquery

PROJECT_ID = 'IntegracaoHomologado'

class Data(Resource):
    def get(self):
        # Initialize BigQuery Client
        client = bigquery.Client()

        # Define SQL query
        query = """
            SELECT name, age FROM `my_project.my_dataset.my_table`
            WHERE age > 18
            LIMIT 10
        """

        query_job = client.query(query)
        results = query_job.result()
        return list([row.email for row in results])


    def post(self):
        conn = db_connect.connect()

        hashed_password = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt())

        # Inserir fornecedor
        conn.execute(text("INSERT INTO Josmar (email, password, budget) VALUES (:email, :password, :budget)"),
            {
                "email": request.json['email'],
                "password": hashed_password,
                "budget": request.json['budget']
            }
        )

        conn.connection.commit()

        # Retornar o fornecedor e endereço inseridos
        query = conn.execute(text('SELECT email, budget FROM Josmar'))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.fetchall()]

        return jsonify(result)