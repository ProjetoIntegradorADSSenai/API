import json
import mysql.connector
from datetime import datetime

'''
def lambda_handler(event, context):
    # TODO implement
    cnx = mysql.connector.connect(
        user='admin', 
        password='adminsenha', 
        host='database-mysql.culoy8hhyeuv.us-east-1.rds.amazonaws.com',
        database='mydb'
    )

    cursor = cnx.cursor()
    create_db_query = "CREATE DATABASE IF NOT EXISTS mydb"
    cursor.execute(create_db_query)
    cnx.commit()

    table_exists_query = 'SHOW TABLES LIKE "mytable"'
    cursor.execute(table_exists_query)
    table_exists = cursor.fetchone()

    if not table_exists:
        create_table_query = "CREATE TABLE mytable (id INT AUTO_INCREMENT PRIMARY KEY, date_time TIMESTAMP, metal INT, plastic INT)"
        cursor.execute(create_table_query)
        cnx.commit()

    insert_query = "INSERT INTO mytable (date_time, metal, plastic) VALUES (%s, %s, %s)"
    # insert_values = (event['date_time'], event['metal'], event['plastic'])
    insert_values = ("2025-03-20 16:31:02", 96, 12)
    # cursor.execute(insert_query, insert_values)
    # cnx.commit()

    select_query = "SELECT * FROM mytable"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table_data = []
    for row in rows:
        table_data.append({
            'id': row[0],
            'date_time': row[1].strftime('%Y-%m-%d %H:%M:%S'),
            'metal': row[2],
            'plastic': row[3]
        })
    json_data = json.dumps(table_data)

    cursor.close()
    cnx.close()

    return {
        'statusCode': 200,
        'body': json_data
    }
'''

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user='admin', 
            password='adminsenha', 
            host='database-mysql.culoy8hhyeuv.us-east-1.rds.amazonaws.com',
            database='mydb'
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
        cursor.execute("SELECT * FROM mytable")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert result to a JSON-serializable format
        table_data = []
        for row in results:
            table_data.append({
                'id': row[0],
                'date_time': row[1].strftime('%Y-%m-%d %H:%M:%S') if row[1] else None,
                'metal': row[2],
                'plastic': row[3]
            })

        json_data = json.dumps(table_data)
        return {
            'statusCode': 200,
            'body': json_data
        }
    except Exception as e:
        return {"error": str(e)}, 500

def post(data):
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}, 500
    try:
        cursor = conn.cursor()
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_query = "INSERT INTO mytable (date_time, metal, plastic) VALUES (%s, %s, %s)"
        insert_values = (time_now, data['metal'], data['plastic'])  # Ensure this is a tuple
        cursor.execute(insert_query, insert_values)
        conn.commit()

        # Fetch the inserted data based on the time
        cursor.execute("SELECT date_time, metal, plastic FROM mytable WHERE date_time = %s", (time_now,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        # Convert result to JSON
        if result:
            result_data = {
                'date_time': result[0].strftime('%Y-%m-%d %H:%M:%S'),
                'metal': result[1],
                'plastic': result[2]
            }
            return json.dumps(result_data)
        else:
            return {"error": "No data found after insertion"}, 500

    except Exception as e:
        return {"error": str(e)}, 500

def lambda_handler(event, context):
    print(event)
    operation = event.get('operation')

    if operation == 'get':
        return get()
    elif operation == 'post':
        return post(event.get('payload'))
    else:
        raise ValueError(f'Unrecognized operation {operation}')