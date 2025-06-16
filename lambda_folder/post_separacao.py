import json
import os
import mysql.connector

def get_db_connection():
    try:
        return mysql.connector.connect(
            user=os.environ['user'],
            password=os.environ['password'],
            host=os.environ['host'],
            database=os.environ['database']
        )
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return None

def lambda_handler(event, context):
    try:
        if 'body' in event:
            body = json.loads(event['body'])
            id_pecas = body['id_pecas']  # O que é esperado -> {"id_pecas": [1,2,3]}
        else:
            id_pecas = event['id_pecas']  # O que é esperado -> {"id_pecas": [1,2,3]}
        
        conn = get_db_connection()
        if not conn:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Database connection failed'})
            }

        cursor = conn.cursor()
        cursor.execute("SET time_zone = 'America/Sao_Paulo';")
        for peca in id_pecas:
            cursor.execute(
                "INSERT INTO separacao (id_peca) VALUES (%s)",
                (peca,)
            )
        conn.commit()
        cursor.close()
        conn.close()

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Separation record created successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }