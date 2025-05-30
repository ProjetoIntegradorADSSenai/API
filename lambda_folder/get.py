import json
import mysql.connector
from datetime import datetime

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user='admin', 
            password='admin123', 
            host='mydb.cvqqiquykhcp.us-east-1.rds.amazonaws.com',
            database='myDB'
        )
        return conn
    except Exception as e:
        return None

def get():
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}, 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.id_peca, s.horario_inicial, s.horario_fim, p.tipo 
            FROM Separacao s
            INNER JOIN Peca p ON s.id_peca = p.id
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert result to a JSON-serializable format
        table_data = []
        for row in results:
            start_dt = row['horario_inicial']
            start_date = start_dt.strftime('%Y-%m-%d') if start_dt else None
            start_time = start_dt.strftime('%H:%M:%S') if start_dt else None
            
            end_dt = row['horario_fim']
            end_date = end_dt.strftime('%Y-%m-%d') if end_dt else None
            end_time = end_dt.strftime('%H:%M:%S') if end_dt else None

            table_data.append({
                'separacao_id': row['id'],
                'peca_id': row['id_peca'],
                'peca_tipo': row['tipo'],
                'inicio_date': start_date,
                'inicio_time': start_time,
                'fim_date': end_date,
                'fim_time': end_time,
                'start_dt': row['horario_inicial'],
                'end_dt': row['horario_fim']
            })

        json_data = json.dumps(table_data)
        return {
            'statusCode': 200,
            'body': json_data
        }
    except Exception as e:
        return {"error": str(e)}, 500

def lambda_handler(event, context):
    return get()