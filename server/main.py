from flask import Flask, render_template, request, redirect, session, jsonify
import psycopg2
# import flask_login
import json
# from config import Config
import numpy as np
from configparser import ConfigParser

app = Flask(__name__, template_folder='../pages', static_folder='../pages')
# app.secret_key = 'your_secret_key'

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

params = config()
conn = psycopg2.connect(**params)

@app.route("/signin", methods=["POST"])
def sign_in():
    cursor = conn.cursor()
    json_in_data = json.loads(request.get_data())
    login = json_in_data["login"]
    password = json_in_data["password"]
    out_data = {}

    data_from_db = cursor.execute("select * from users where login = '{0}' and password = '{1}'".format(login, password))
    data_from_db = cursor.fetchone()
    # print(data_from_db)

    if data_from_db is None:
        out_data["user_found"] = False
    else:
        out_data["user_found"] = True
        out_data["status"] = data_from_db[1]

    return json.dumps(out_data)

@app.route("/products", methods=["POST"])
def get_products():
    cursor = conn.cursor()
    out_data = []
    data_from_db = cursor.execute("select * from products where type = 'товар'")
    data_from_db = cursor.fetchall()

    '''
    category = cursor.execute("select * from products_categories where type = 'товар'")
    category = cursor.fetchall()
    categories = {}
    for i in range(len(category)):
        categories[category[i][0]] = category[i][1]
    '''

    categories = {1: "Гроб", 2: "Венок", 3: "Табличка", 4: "Крест"}

    if data_from_db is None:
        out_data.append({})
        out_data[0]["products_found"] = False
    else:
        out_data.append({})
        out_data[0]["products_found"] = True
        for i in range(1, len(data_from_db) + 1):
            out_data.append({})
            out_data[i]["id"] = data_from_db[i - 1][0]
            out_data[i]["category"] = categories[data_from_db[i - 1][2]]
            out_data[i]["amount"] = data_from_db[i - 1][3]
            out_data[i]["cost_for_one"] = data_from_db[i - 1][4]
            out_data[i]["details"] = data_from_db[i - 1][5]

    return json.data(out_data)

@app.route("/services", methods=["POST"])
def get_services():
    cursor = conn.cursor()
    out_data = []
    data_from_db = cursor.execute("select * from products where type = 'услуга'")
    data_from_db = cursor.fetchall()

    '''
    category = cursor.execute("select * from products_categories where type = 'услуга'")
    category = cursor.fetchall()
    categories = {}
    for i in range(len(category)):
        categories[category[i][0]] = category[i][1]
    '''

    categories = {5: "Гробовщик", 6: "Бальзамировщик", 7: "Водитель", 8: "Священник", 9: "Психолог"}

    if data_from_db is None:
        out_data.append({})
        out_data[0]["services_found"] = False
    else:
        out_data.append({})
        out_data[0]["services_found"] = True
        for i in range(1, len(data_from_db) + 1):
            out_data.append({})
            out_data[i]["id"] = data_from_db[i - 1][0]
            out_data[i]["category"] = categories[data_from_db[i - 1][2]]
            out_data[i]["cost_for_one"] = data_from_db[i - 1][4]

    return json.dump(out_data)

#conn.close()
if __name__ == '__main__':
    # app = Flask(__name__, template_folder='../pages', static_folder='../pages')
    app.run(debug=True, host="127.0.0.1")