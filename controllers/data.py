from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import boto3

# Configuração do Flask
app = Flask(__name__)
api = Api(app)

# Configuração do banco de dados PostgreSQL
DB_HOST = "database-2.clhwd5ytyuym.us-east-1.rds.amazonaws.com"
DB_PORT = 5432  # Porta padrão do PostgreSQL
DB_USER = "postgres"
DB_NAME = "database-2"
REGION = "us-east-1c"
DB_PASS = "Senhapost"

# Cria sessão boto3 para gerar token de autenticação
session = boto3.Session(profile_name='RDSCreds')
client = session.client('rds')

# Função para criar uma conexão com o banco de dados PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslrootcert="SSLCERTIFICATE"
    )

class Data(Resource):
    def get(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM Data")
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(results)
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        try:
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                "INSERT INTO Data (time, metal, plastic) VALUES (%s, %s, %s)",
                (time_now, data['metal'], data['plastic'])
            )
            conn.commit()

            # Recupera o registro inserido
            cursor.execute(
                "SELECT time, metal, plastic FROM Data WHERE time = %s",
                (time_now,)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return jsonify(result)
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(Data, '/data')

if __name__ == '__main__':
    app.run(debug=True)