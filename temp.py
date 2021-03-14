from flask import Flask
import sqlite3
conn = sqlite3.connect('hackers.db')

c = conn.cursor()

c.execute("""CREATE TABLE employees (
            first text,
            last text,
            pay integer
            )""")


c.execute("INSERT INTO employees VALUES ('Corey', 'Schafer', 50000)")

c.execute("SELECT * FROM employees WHERE last='Schafer'")

c.fetchone() # c.fetchmany(number) c.fetchall()

conn.commit() 

conn.close()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

