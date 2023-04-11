import psycopg2
from flask import Flask, redirect, url_for, render_template, request
import json
from config import Config
import numpy as np
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def connect():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        print(params)
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)
        
        cur.close()
    except (Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print("error")
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
        else:
            print('Database connection failed for some reason')


if __name__ == '__main__':
    app = Flask(__name__, template_folder='./pages', static_folder='./pages')
    connection = connect()
    cursor = connection.cursor()



'''
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/managerapplication")
def managerApplication():
    return render_template("managerApplication.html")

@app.route("/managerservices")
def managerServices():
    return render_template("managerServices.html")

@app.route("/managerstorage")
def managerStorage():
    return render_template("managerStorage.html")

@app.route("/signin", methods=["POST"])
def manager_log_in():
    json_in_data = json.loads(request.get_data())
    login = json_in_data["login"]
    password = json_in_data["password"]
    answer = {}
    data = ''

    data_from_db = cursor.execute("select * from users where login = login")

    if len(data_from_db) == 0:
        answer["empty_error"] = True
        answer["data"] = data
    else:
        data = data_from_db
        answer["empty_error"] = False
        answer["data"] = data
        answer["status"] = data_from_db[1]
        answer["login"] = data_from_db[2]
        answer["password"] = data_from_db[3]
        answer["name"] = data_from_db[4]
        answer["email"] = data_from_db[5]
        answer["phone"] = data_from_db[6]

    return json.dump(answer)


@app.route("/getservices", methods=["POST"])
def get_services():
    json_in_data = json.loads(request.get_data())
    service_type = json_in_data["service_name"]
    answer = {}
    data = ''
    data_from_db = cursor.execute("select * from products where type = service")
    
    if len(data_from_db) == 0:
        answer["empty_error"] = True
        answer["data"] = data
    else:
        data = data_from_db
        answer["empty_error"] = False
        answer["data"] = data
        answer["category"] = data_from_db[2]
        answer["amount"] = data_from_db[3]
        answer["cost_for_one"] = data_from_db[4]
        answer["details"] = data_from_db[5]

    return json.dump(answer)


@app.route("/getproducts", methods=["POST"])
def get_products():
    json_in_data = json.loads(request.get_data())
    service_type = json_in_data["product_name"]
    answer = {}
    data = ''
    data_from_db = cursor.execute("select * from products where type = product")
    
    if len(data_from_db) == 0:
        answer["empty_error"] = True
        answer["data"] = data
    else:
        data = data_from_db
        answer["empty_error"] = False
        answer["data"] = data
        answer["category"] = data_from_db[2]
        answer["amount"] = data_from_db[3]
        answer["cost_for_one"] = data_from_db[4]
        answer["details"] = data_from_db[5]

    return json.dump(answer)


connection.close()

if __name__ == "__main__":
    app.run(debug=True)'''