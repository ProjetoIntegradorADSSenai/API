import json
import mysql.connector
from datetime import datetime

cnx = mysql.connector.connect(
    user='admin', 
    password='adminsenha', 
    host='mydb.culoy8hhyeuv.us-east-1.rds.amazonaws.com',
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
cursor.execute(insert_query, insert_values)
cnx.commit()

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

print(table_data)