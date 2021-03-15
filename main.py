from flask import (Flask, jsonify, request)
import sqlite3
import json

# opens json file with data
with open('hacker-data-2021.json') as data: 
    hackersData = json.load(data)

# creates connection & cursor
# :memory: means database in created every time program runs
conn = sqlite3.connect(':memory:', check_same_thread=False)
# below is an option if you want to save to file instead
# conn = sqlite3.connect('hackers.db', check_same_thread=False)
c = conn.cursor()

# creates main table, with hacker data
c.execute("""CREATE TABLE hackers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            picture TEXT, 
            company TEXT,
            email TEXT,
            phone TEXT
            )""")
# creates second table with skills, each skill referencing a hacker in first table
c.execute("""CREATE TABLE skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hacker_id INTEGER,
            name TEXT,
            rating INTEGER,
            FOREIGN KEY (hacker_id) REFERENCES hackers (id)
            )""")
conn.commit()

# inserting hacker data and skills data into database
for hacker in hackersData:
    c.execute("INSERT INTO hackers VALUES (NULL, ?, ?, ?, ?, ?)",
        [hacker['name'], hacker['picture'], hacker['company'], hacker['email'], hacker['phone']])
    foreign_key = c.lastrowid
    skills = hacker['skills']
    for skill in skills:
        c.execute("INSERT INTO skills VALUES (NULL, ?, ?, ?)",
        [foreign_key, skill['name'], skill['rating']])
    conn.commit()

app = Flask(__name__)

# default
@app.route('/')
def home():
    return "Hello!"

# (1) ALL USERS ENDPOINT 
@app.route('/users', methods=['GET'])
def create_db():
    c.execute("SELECT * FROM hackers INNER JOIN skills ON hackers.id = skills.hacker_id")
    result = c.fetchall()
    conn.commit()
    return jsonify(result)

# (2) USER INFORMATION ENDPOINT & (3) UPDATE USER DATA ENDPOINT
@app.route('/users/<id>', methods=['GET', 'PUT'])
def get_user_info(id):
    if request.method == 'GET': # getting hacker (& skill) information based on ID
        c.execute("SELECT * FROM hackers INNER JOIN skills ON hackers.id = skills.hacker_id WHERE hackers.id='%s'" % id)
        result = c.fetchall()
        conn.commit()
        return jsonify(result)
    else:
        c.execute("SELECT * FROM hackers WHERE id='%s'" % id) # getting hacker information
        user_data = c.fetchall()
        request_data = request.get_json() # getting information from put request 
        user = { # calls update_helper(put request data, data name, current data)
            'name': update_helper(request_data, 'name', user_data[0][1]),
            'picture': update_helper(request_data, 'picture', user_data[0][2]),
            'company': update_helper(request_data, 'company', user_data[0][3]),
            'email': update_helper(request_data, 'email', user_data[0][4]),
            'phone': update_helper(request_data, 'phone', user_data[0][5])
        }
        c.execute("""UPDATE hackers SET name=?, picture=?, company=?, email=?, phone=? WHERE id=?""", # updates data 
                    [user['name'], user['picture'], user['company'], user['email'], user['phone'], id])
        conn.commit()
        c.execute("SELECT * FROM hackers INNER JOIN skills ON hackers.id = skills.hacker_id WHERE hackers.id='%s'" % id)
        result = c.fetchall()
        conn.commit()
        return jsonify(result)

# helper function for PUT request - returns default data if no new one is sent
def update_helper(request_data, data_point, default):
    # if no data sent, return default 
    if request_data == None:
        return default
    try:
        # if can find this specific data point in request_data
        res = request_data[data_point]
        return res
    # means there is new data, but not for this point - return default
    except KeyError:
        return default

# (4) SKILLS ENDPOINT
@app.route('/skills', methods=['GET'])
def get_skills():
    try: 
        min_frequency = request.args.get('min_frequency')
        max_frequency = request.args.get('max_frequency')
        # with query parameters 
        # returns skills with frequency between given min and max
        if min_frequency and max_frequency:
            c.execute("SELECT name, COUNT(*) FROM skills GROUP BY name HAVING COUNT(*) > %s AND COUNT(*) < %s" % (min_frequency, max_frequency))
        # return skills with frequency over min
        elif min_frequency:
            c.execute("SELECT name, COUNT(*) FROM skills GROUP BY name HAVING COUNT(*) > %s" % (min_frequency))
        # return skills with frequence under max
        elif max_frequency:
            c.execute("SELECT name, COUNT(*) FROM skills GROUP BY name HAVING COUNT(*) < %s" % (max_frequency))
        # with no query parameters
        # returns all skills with frequencies of each
        else:
            c.execute("SELECT name, COUNT(*) FROM skills GROUP BY name")
        result = c.fetchall()
        conn.commit()
        return jsonify(result)
    except Exception as e:
        print(e)
        return "An error occured."

# runs flask app 
if __name__ == "__main__":
    app.run(debug=True)