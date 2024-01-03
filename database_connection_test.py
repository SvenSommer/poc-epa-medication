import psycopg2

conn = psycopg2.connect(
    dbname="fhir_resources",
    user="medication_service",
    password="secret_password",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

