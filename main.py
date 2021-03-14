from flask import (Flask, jsonify, request)
import sqlite3

# https://www.programiz.com/python-programming/json
import json
with open('hacker-data-2021.json') as data: 
    hackersData = json.load(data)

conn = sqlite3.connect(':memory:', check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE hackers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            picture TEXT, 
            company TEXT,
            email TEXT,
            phone TEXT
            )""")
c.execute("""CREATE TABLE skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hacker_id INTEGER,
            name TEXT,
            rating INTEGER,
            FOREIGN KEY (hacker_id) REFERENCES hackers (id)
            )""")
conn.commit()

for hacker in hackersData:
    c.execute("INSERT INTO hackers VALUES (NULL, ?, ?, ?, ?, ?)",
        [hacker['name'], hacker['picture'], hacker['company'], hacker['email'], hacker['phone']])
    foreign_key = c.lastrowid
    skills = hacker['skills']
    for skill in skills:
        c.execute("INSERT INTO skills VALUES (NULL, ?, ?, ?)",
        [foreign_key, skill['name'], skill['rating']])
    conn.commit()



#c.execute("SELECT * FROM hackers WHERE name='Stephens Terrell'")
#print(c.fetchall())
#conn.commit()


# c.execute("INSERT INTO hackers VALUES ('Name', 'Picture', 'Company', '12345')")
# conn.commit() 

# c.execute("SELECT * FROM hackers WHERE name='Name'")

# print(c.fetchall())
# conn.commit()

# conn.close()

app = Flask(__name__)

@app.route('/')
def create_db():
    c.execute("SELECT * FROM hackers INNER JOIN skills ON hackers.id = skills.hacker_id")
    result = c.fetchall()
    #c.execute("SELECT * FROM skills")
    #result2 = c.fetchall()
    conn.commit()
    return jsonify(result)

@app.route('/users/<id>', methods=['GET', 'PUT'])
def get_user_info(id):
    if request.method == 'GET':
        c.execute("SELECT * FROM hackers INNER JOIN skills ON hackers.id = skills.hacker_id WHERE hackers.id='%s'" % id)
        result = c.fetchall()
        conn.commit()
        return jsonify(result)
    else:
        c.execute("SELECT * FROM hackers WHERE id='%s'" % id)
        user_data = c.fetchall()
        #c.execute("SELECT * FROM skills WHERE hacker_id='%s'" % id)
        #skills_data = c.fetchall()
        #print(user_data)
        #print(user_data[0][2])
        request_data = request.get_json()
        user = {
            'name': update_helper(request_data, 'name', user_data[0][1]),
            'picture': update_helper(request_data, 'picture', user_data[0][2]),
            'company': update_helper(request_data, 'company', user_data[0][3]),
            'email': update_helper(request_data, 'email', user_data[0][4]),
            'phone': update_helper(request_data, 'phone', user_data[0][5])
        }
        #print(user)
        c.execute("""UPDATE hackers SET name=?, picture=?, company=?, email=?, phone=? WHERE id=?""",
                    [user['name'], user['picture'], user['company'], user['email'], user['phone'], id])
        conn.commit()
        c.execute("SELECT * FROM hackers INNER JOIN skills ON hackers.id = skills.hacker_id WHERE hackers.id='%s'" % id)
        result = c.fetchall()
        conn.commit()
        return jsonify(result)

def update_helper(request_data, data_point, default):
    if request_data == None:
        return default
    try:
        res = request_data[data_point]
        return res
    except KeyError:
        return default

