# import neccessary modules
from flask import Flask, request, jsonify
import sqlite3

#create an app instance
app = Flask(__name__)

# set up a function for connecting database
def database ():
    try:
        connect_db = sqlite3.connect('database.sqlite')
        print('Database connected successfully')
        return connect_db
    except Exception as e:
        print (f'database cannot connect because of: {e}')

# Create a table in the database
def create_table ():
    try:
        db = database()
        query = """CREATE TABLE IF NOT EXISTS auth(
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
                )"""
        db.execute(query)
        db.commit()
        db.close()
        print ('Table created successfully')
    except Exception as e:
        print (f'Table cannot be created because of: {e}')
    
create_table()

# insert data in the table
def insert_data(username, email, password):
    try:
        db = database()
        query = """INSERT INTO auth(username, email, password) VALUES(?, ?, ?)"""
        db.execute(query, (username, email, password))
        db.commit()
        db.close()
        print('Data inserted to auth table is successful')
    except Exception as e:
        print (f'Data cannot be inserted because of: {e}')

# fetch all data in the database
def fetchall_data():
    db = database()
    query = """SELECT * FROM auth"""
    data = db.execute(query)
    data_dic = data.fetchall()
    return(data_dic)

def db_data():
    data_array = fetchall_data()
    data_dic_array = []
    for i in range(len(data_array)):
        data_dic = {
            "id": data_array[i][0],
            "username": data_array[i][1],
            "email": data_array[i][2],
            "password": data_array[i][3]
        }
        data_dic_array = data_dic_array + [data_dic]
    return (data_dic_array)


# create the home page route
@app.route('/')
def home():
    return ("Welcome to Adesina's Authentication API. Created on November 27, 2024 !")

# create a sign up route
@app.route('/signup', methods=['POST'])
def signup ():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    insert_data(username, email, password)
    return jsonify({
        "status": "success",
        "message": "Signup Successful"
    }), 200

# Create the login route
@app.route('/login', methods=['POST'])
def login ():
    username = request.form.get('username')
    password = request.form.get('password')

    data = db_data()
    for i in range(len(data)):
        if data[i]['username'] == username and data[i]['password'] == password:
            return jsonify({
                "status": "success",
                "message": "Login Successful"
            }), 200       
    return jsonify({
        "status": "error",
        "message": "Invalid username or password"
    }), 401


if __name__ == '__main__':
    app.run(port=8000, debug=True)
