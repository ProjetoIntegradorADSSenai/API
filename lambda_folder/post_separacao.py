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
            id_peca = body['id_peca']  # O que é esperado -> {"id_peca": 1, "horario_fim": "2023-10-01 12:00:00"}
            horario_fim = body['horario_fim']  # Opcional (o horário de início é gerado automaticamente pelo banco)
        else:
            id_peca = event['id_peca']  # O que é esperado -> {"id_peca": 1, "horario_fim": "2023-10-01 12:00:00"}
            horario_fim = event['horario_fim']  # Opcional (o horário de início é gerado automaticamente pelo banco)
        
        conn = get_db_connection()
        if not conn:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Database connection failed'})
            }

        cursor = conn.cursor()
        # Timezone do Brasil
        cursor.execute("SET time_zone = 'America/Sao_Paulo';")
        if horario_fim:
            cursor.execute(
                "INSERT INTO separacao (id_peca, horario_fim) VALUES (%s, %s)",
                (id_peca, horario_fim)
            )
        else:
            cursor.execute(
                "INSERT INTO separacao (id_peca) VALUES (%s)",
                (id_peca,)
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