from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pymysql

# Flask app setup
app = Flask(__name__)
api = Api(app)

# Database configuration
DB_HOST = "database-1.clhwd5ytyuym.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "RDS_project"
DB_NAME = "database-1"

# Function to create a database connection
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

class Data(Resource):
    def get(self):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Data")
                results = cursor.fetchall()
            conn.close()
            return jsonify(results)
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        try:
            data = request.json

            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Data (time, metal, plastic) VALUES (%s, %s, %s)",
                    (data['time'], data['metal'], data['plastic'])
                )
                conn.commit()

                # Retrieve the inserted record
                cursor.execute("SELECT time, metal, plastic FROM Data WHERE time = %s", (data['time'],))
                result = cursor.fetchone()

            conn.close()
            return jsonify(result)

        except Exception as e:
            return {"error": str(e)}, 500