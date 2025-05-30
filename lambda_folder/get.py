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
        cursor.execute("""
            SELECT 
                peca_tipo,
                time_interval,
                DATE(time_interval) AS date,
                TIME(time_interval) AS time,
                total_separacoes,
                avg_duration_seconds,
                min_duration,
                max_duration
            FROM agregacao
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }
    except Exception as e:
        return {"error": str(e)}, 500

def lambda_handler(event, context):
    return get()