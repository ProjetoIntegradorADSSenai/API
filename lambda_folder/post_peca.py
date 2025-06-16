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
            tipos = body['tipos']
        else:
            tipos = event['tipos']

        id_pecas = []

        conn = get_db_connection()
        if not conn:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Database connection failed'})
            }

        cursor = conn.cursor()
        cursor.execute("SET time_zone = 'America/Sao_Paulo';")
        for peca in tipos:
            cursor.execute("INSERT INTO peca (tipo) VALUES (%s)", (peca,))
            cursor.execute("SELECT LAST_INSERT_ID();")
            id_pecas.append(cursor.fetchone()[0])

        conn.commit()
        cursor.close()
        conn.close()

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Part created successfully',
                'id_peca': id_pecas
            })
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing "tipos" in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }