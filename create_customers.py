from werkzeug.security import generate_password_hash
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='smart_erp'
)
cursor = conn.cursor()

customers = [
    ('Ravi Kumar',    'ravi@gmail.com',  '9876543210', 'ravi123'),
    ('Priya Sharma',  'priya@gmail.com', '9123456780', 'priya123'),
    ('Walk-in Customer', '',             '',           'walkin123'),
]

for name, email, phone, pwd in customers:
    hashed = generate_password_hash(pwd)
    cursor.execute("""
        INSERT INTO customers (customer_name, email, phone, password)
        VALUES (%s, %s, %s, %s)
    """, (name, email, phone, hashed))

conn.commit()
cursor.close()
conn.close()
print("Customers created successfully!")