import psycopg2
engine = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="Senhapost",
    host="database-2.clhwd5ytyuym.us-east-1.rds.amazonaws.com",
    port='5432'
)