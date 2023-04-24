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

@app.route("/signIn", methods=["POST"])
def signIn():
    cursor = conn.cursor()
    jsonInData = json.loads(request.get_data())
    login = jsonInData["login"]
    password = jsonInData["password"]
    outData = {}

    dataFromDb = cursor.execute("select * from users where login = '{0}' and password = '{1}'".format(login, password))
    dataFromDb = cursor.fetchone()

    if dataFromDb is None:
        outData["userFound"] = False
    else:
        outData["userFound"] = True
        outData["status"] = dataFromDb[1]

    return json.dumps(outData)

@app.route("/products", methods=["POST"])
def getProducts():
    cursor = conn.cursor()
    outData = []
    dataFromDb = cursor.execute("select * from products where type = 'товар'")
    dataFromDb = cursor.fetchall()

    categoriesFromDb = cursor.execute("select * from products_categories")
    categoriesFromDb = cursor.fetchall()
    categories = {}
    for i in range(len(categoriesFromDb)):
        categories[categoriesFromDb[i][0]] = categoriesFromDb[i][1]

    if dataFromDb is None:
        outData.append({})
        outData[0]["productsFound"] = False
    else:
        outData.append({})
        outData[0]["products_found"] = True
        for i in range(1, len(dataFromDb) + 1):
            if dataFromDb[i - 1][3] > 0:
                outData.append({})
                outData[i]["id"] = dataFromDb[i - 1][0]
                outData[i]["category"] = categories[dataFromDb[i - 1][2]]
                outData[i]["amount"] = dataFromDb[i - 1][3]
                outData[i]["costForOne"] = dataFromDb[i - 1][4]
                outData[i]["details"] = dataFromDb[i - 1][5]
                outData[i]["imageLink"] = dataFromDb[i - 1][6]

    return json.dumps(outData)

@app.route("/services", methods=["POST"])
def getServices():
    cursor = conn.cursor()
    outData = []
    dataFromDb = cursor.execute("select * from products where type = 'услуга'")
    dataFromDb = cursor.fetchall()

    categoriesFromDb = cursor.execute("select * from products_categories")
    categoriesFromDb = cursor.fetchall()
    categories = {}
    for i in range(len(categoriesFromDb)):
        categories[categoriesFromDb[i][0]] = categoriesFromDb[i][1]

    if dataFromDb is None:
        outData.append({})
        outData[0]["servicesFound"] = False
    else:
        outData.append({})
        outData[0]["servicesFound"] = True
        for i in range(1, len(dataFromDb) + 1):
            outData.append({})
            outData[i]["id"] = dataFromDb[i - 1][0]
            outData[i]["category"] = categories[dataFromDb[i - 1][2]]
            outData[i]["costForOne"] = dataFromDb[i - 1][4]

    return json.dumps(outData)

@app.route("/ordersForManager", methods=["POST"])
def getOrdersForManager():
    cursor = conn.cursor()
    outData = []
    dataFromDb = cursor.execute("select * from orders")
    dataFromDb = cursor.fetchall()

    clientsFromDb = cursor.execute("select * from users where status = 'клиент'")
    clientsFromDb = cursor.fetchall()
    clientsFio = {}
    for i in range(len(clientsFromDb)):
        clientsFio[clientsFromDb[i][0]] = clientsFromDb[i][4]

    if dataFromDb is None:
        outData.append()
        outData[0]["ordersFound"] = False
    else:
        outData.append({})
        outData[0]["ordersFound"] = True
        for i in range(1, len(dataFromDb) + 1):
            outData.append({})
            outData[i]["id"] = dataFromDb[i - 1][0]
            outData[i]["clientsFio"] = clientsFio[dataFromDb[i - 1][1]]
            outData[i]["price"] = dataFromDb[i - 1][3]
            outData[i]["status"] = dataFromDb[i - 1][4]
            outData[i]["address"] = dataFromDb[i - 1][5]
            outData[i]["deadmansName"] = dataFromDb[i - 1][6]
            outData[i]["deadmansPassport"] = dataFromDb[i - 1][7]

    return json.dumps(outData)

@app.route("/ordersOfClient", methods=["POST"])
def getOrdersOfClient():
    cursor = conn.cursor()
    jsonInData = json.loads(request.get_data())
    clientId = jsonInData["client_id"]
    outData = []

    dataFromDb = cursor.execute("select * from orders where client_ID = '{0}'".format(clientId))
    dataFromDb = cursor.fetchall()

    managersFromDb = cursor.execute("select * from users where status = 'менеджер'")
    managersFromDb = cursor.fetchall()
    managersFio = {}
    for i in range(len(managersFromDb)):
        managersFio[managersFromDb[i][0]] = managersFromDb[i][4]

    if dataFromDb is None:
        outData.append({})
        outData[0]["ordersFound"] = False
    else:
        outData.append({})
        outData[0]["ordersFound"] = True
        for i in range(1, len(dataFromDb) + 1):
            outData.append({})
            outData[i]["id"] = dataFromDb[i - 1][0]
            outData[i]["managerFio"] = managersFio[dataFromDb[i - 1][1]]
            outData[i]["price"] = dataFromDb[i - 1][3]
            outData[i]["status"] = dataFromDb[i - 1][4]
            outData[i]["address"] = dataFromDb[i - 1][5]
            outData[i]["deadmansName"] = dataFromDb[i - 1][6]
            outData[i]["deadmansPassport"] = dataFromDb[i - 1][7]

    return json.dumps(outData)
    
@app.route("/allProducts", methods=["POST"])
def getProductsAndServices():
    cursor = conn.cursor()
    outData = []
    dataFromDb = cursor.execute("select * from products")
    dataFromDb = cursor.fetchall()

    categoriesFromDb = cursor.execute("select * from products_categories")
    categoriesFromDb = cursor.fetchall()
    categories = {}
    for i in range(len(categoriesFromDb)):
        categories[categoriesFromDb[i][0]] = categoriesFromDb[i][1]

    if dataFromDb is None:
        outData.append({})
        outData[0]["itemsFound"] = False
    else:
        outData.append({})
        outData[0]["itemsFound"] = True
        for i in range(1, len(dataFromDb) + 1):
            outData.append({})
            outData[i]["id"] = dataFromDb[i - 1][0]
            outData[i]["type"] = dataFromDb[i - 1][1]
            outData[i]["category"] = categories[dataFromDb[i - 1][2]]
            outData[i]["amount"] = dataFromDb[i - 1][3]
            outData[i]["costForOne"] = dataFromDb[i - 1][4]
            outData[i]["details"] = dataFromDb[i - 1][5]
            outData[i]["imageLink"] = dataFromDb[i - 1][6]

    return json.dumps(outData)

'''
@app.route("/productsToOrder", methods=["POST"])
def insertProductsToBuy():
    cursor = conn.cursor()
    jsonInData = json.loads(request.get_data())
    inDataCategory = jsonInData["product_category"]
    inDataName = jsonInData["product_name"]
    inDataAmount = jsonInData["product_amount"]

    categoriesFromDb = cursor.execute("select * from products_categories")
    categoriesFromDb = cursor.fetchall()
    categories = {}
    for i in range(len(categoriesFromDb)):
        categories[categoriesFromDb[i][1]] = categoriesFromDb[i][0]
    
    dataToDb = {}
    #dataToDb["product_category"] = categories[inDataCategory]
    
    dataToDb["product_id"] = 
    dataToDb["amount"] = inDataAmount
'''

#conn.close()
if __name__ == '__main__':
    # app = Flask(__name__, template_folder='../pages', static_folder='../pages')
    app.run(debug=True, host="127.0.0.1")