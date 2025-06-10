import os
import json
import mysql.connector
from datetime import datetime

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

def get():
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}, 500
    try:
        cursor = conn.cursor(dictionary=True)
        # Timezone do Brasil
        cursor.execute("SET time_zone = 'America/Sao_Paulo';")        
        cursor.execute("""
            SELECT 
                peca_tipo,
                time_interval,
                DATE_FORMAT(time_interval, '%Y-%m-%d') AS date,
                DATE_FORMAT(time_interval, '%H:%i:%s') AS time,
                total_separacoes
            FROM agregacao
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Group results by time_interval
        grouped_results = {}
        for row in results:
            interval = row['time_interval']
            if interval not in grouped_results:
                grouped_results[interval] = []
            grouped_results[interval].append(row)

        # Convert to list of arrays
        final_output = list(grouped_results.values())

        return {
            'statusCode': 200,
            'body': json.dumps(final_output, default=str)
        }
    except Exception as e:
        return {"error": str(e)}, 500

def lambda_handler(event, context):
    return get()