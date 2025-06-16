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
            devices = body['dispositivos'] # Espera -> { 'dispositivos': {'sensor_1': true, 'sensor_2': false, ...} }
        else:
            devices = event['dispositivos']

        conn = get_db_connection()
        if not conn:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Database connection failed'})
            }

        cursor = conn.cursor()
        for key, value in devices.items():
            cursor.execute("UPDATE dispositivos SET estado = %s WHERE nome = %s", (value, key))

        conn.commit()
        cursor.close()
        conn.close()

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Devices updated successfully',
            })
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing "dispositivos" in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }