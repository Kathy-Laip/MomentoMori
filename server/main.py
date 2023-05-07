from flask import Flask, render_template, request, redirect, session, jsonify
import psycopg2
# import flask_login
import json
import numpy as np
from configparser import ConfigParser

app = Flask(__name__, template_folder='../pages', static_folder='../pages')
# app.secret_key = 'your_secret_key'


'''
Функция, возвращающая параметры базы данных для подключения.
'''
def config(filename='datababase.ini', section='postgresql'):
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


'''
Функция для авторизации пользователя. Принимает логин и пароль для входа, возвращает информацию, найден ли пользователь,
его статус и id, если найден.
'''
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
        outData["id"] = dataFromDb[0]

    return json.dumps(outData)


'''
Функция получения информации о товарах в наличии. Ничего не принимает, возвращает информацию, найдены ли товары в наличии, и массив данных 
о найденных товарах: id товара, категория, количество на складе, стоимость за единицу товара, детали и ссылку на картинку товара.
'''
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
        outData[0]["productsFound"] = True
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


'''
Функция получения информации о доступных услугах. Ничего не принимает, возвращает информацию о том, найдены ли услуги, и массив данных
о доступных услугах: id услуги, категория, стоимость услуги.
'''
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


'''
Функция получения информации обо всех заказах для менеджера. Ничего не получает, возвращает информацию о том, найдены ли заказы, и массив данных
о найденных заказах: id заказа, ФИО заказчика, общую стоимость, статус заказа, адрес доставки, ФИО покойного, данные паспорта покойного.
'''
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


'''
Функция получения информации обо всех заказах клиента. Получает id клиента, возвращает информацию о том, найдены ли заказы, и массив данных
о найденных заказах: id заказа, ФИО менеджера, общая стоимость, статус заказа, адрес доставки, ФИО покойного, данные паспорта покойного.
'''
@app.route("/ordersOfClient", methods=["POST"])
def getOrdersOfClient():
    cursor = conn.cursor()
    jsonInData = json.loads(request.get_data())
    clientId = jsonInData["clientId"]
    outData = []

    dataFromDb = cursor.execute('select * from orders where "client_ID" = {0}'.format(clientId))
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
            outData[i]["managerFio"] = managersFio[dataFromDb[i - 1][2]]
            outData[i]["price"] = dataFromDb[i - 1][3]
            outData[i]["status"] = dataFromDb[i - 1][4]
            outData[i]["address"] = dataFromDb[i - 1][5]
            outData[i]["deadmansName"] = dataFromDb[i - 1][6]
            outData[i]["deadmansPassport"] = dataFromDb[i - 1][7]

    return json.dumps(outData)


'''
Функция получения информации обо всех товарах и услугах. Ничего не получает, возвращает информацию о том, найдены ли товары и услуги, и массив
данных о найденных товарах и услугах: id, тип, категория, количество, стоимость единицы, детали, ссылка на изображение.
'''
@app.route("/allProducts", methods=["POST"])
def getProductsAndServices():
    cursor = conn.cursor()
    outData = []
    dataFromDb = cursor.execute("select * from products")
    dataFromDb = cursor.fetchall()

    categoriesFromDb = cursor.execute("select * from products_categories")
    categoriesFromDb = cursor.fetchall()
    categories = {}
    allCategories = []
    for i in range(len(categoriesFromDb)):
        categories[categoriesFromDb[i][0]] = categoriesFromDb[i][1]
        allCategories.append(categoriesFromDb[i][1])

    # print(allCategories)
    if dataFromDb is None:
        outData.append({})
        outData[0]["itemsFound"] = False
    else:
        outData.append({})
        outData[0]["itemsFound"] = True
        outData.append({})
        outData[1]["products"] = allCategories
        for i in range(2, len(dataFromDb) + 2):
            outData.append({})
            outData[i]["id"] = dataFromDb[i - 2][0]
            outData[i]["type"] = dataFromDb[i - 2][1]
            outData[i]["category"] = categories[dataFromDb[i - 2][2]]
            outData[i]["amount"] = dataFromDb[i - 2][3]
            outData[i]["costForOne"] = dataFromDb[i - 2][4]
            outData[i]["details"] = dataFromDb[i - 2][5]
            outData[i]["imageLink"] = dataFromDb[i - 2][6]

    return json.dumps(outData)


'''
Функция проверки количества определенного товара на складе для формирования заявки. Принимает id товара и желаемое количество. 
Возвращает информацию о том, достаточно ли количества, а также количество на складе, если не достаточно.
'''
@app.route("/checkAmount", methods=["POST"])
def checkAmountInStorage():
    cursor = conn.cursor()
    jsonInData = json.loads(request.get_data())
    productId = jsonInData["productId"]
    desiredAmount = jsonInData["productAmount"]
    outData = {}
    
    dataFromDb = cursor.execute("select amount from products where id = {0}".format(productId))
    dataFromDb = cursor.fetchone()

    if dataFromDb[0] >= int(desiredAmount):
        outData["enoughAmount"] = True
    else:
        outData["enoughAmount"] = False
        outData["amountInStorage"] = dataFromDb[0]
    # print(outData)

    return json.dumps(outData)


app.route("/addOrder", methods = ["POST"])
def addOrderToDb():
    cursor = conn.cursor()
    jsonInData = json.loads(request.get_data())
    inAddress = jsonInData['info']['address']
    inClientName = jsonInData['info']['clientName']
    inDeadmansPassport = jsonInData['info']['dataPassport']
    inPhoneClient = jsonInData['info']['phoneClient']
    inDateOfDeath = jsonInData['info']['dateOfDeath']
    inManagerId = jsonInData['info']['managerID']
    inDeadmansName = jsonInData['info']['nameDeceased']

    inProducts = []
    totalPrice = 0
    for i, prod in enumerate(jsonInData['products']):
        inProducts.append({})
        inProducts[i]['category'] = prod['category']
        inProducts[i]['details'] = prod['details']
        inProducts[i]['productId'] = prod['id']
        inProducts[i]['productPrice'] = prod['pr']
        totalPrice += prod['pr']
        inProducts[i]['count'] = prod['count']
    
    '''
    inAddress = 'adddddresssss'
    inClientName = 'cliiiiient name'
    inDeadmansPassport = 'deadmansport'
    inPhoneClient = "89462718496"
    inDateOfDeath = 'dateeeee of death'
    inManagerId = 3
    inDeadmansName = 'deadnaaame'
    '''

    dataToDb = {}

    client_id = cursor.execute(f"select id from users where phone = '{inPhoneClient}'")
    client_id = cursor.fetchone()
    dataToDb['client_ID'] = client_id[0]
    dataToDb['manager_ID'] = inManagerId
    dataToDb['price'] = 12300
    dataToDb['status'] = 'в обработке'
    dataToDb['address'] = inAddress
    dataToDb['deadmans_name'] = inDeadmansName
    dataToDb['deadmans_passport'] = inDeadmansPassport

    try:
        cursor.execute(f"insert into orders (\"client_ID\", \"manager_ID\", price, status, address, deadmans_name, deadmans_passport) values ({dataToDb['client_ID']}, {dataToDb['manager_ID']}, {dataToDb['price']}, '{dataToDb['status']}', '{dataToDb['address']}', '{dataToDb['deadmans_name']}', '{dataToDb['deadmans_passport']}')")
        orderAddedFlag = True
        print('order added')
    except:
        orderAddedFlag = False
        print('order was not added')
    
    orderId = cursor.execute("select max(id) from orders")
    orderId = cursor.fetchone()

    for i, prod in enumerate(jsonInData['products']):
        inProducts.append({})
        inProducts[i]['category'] = prod['category']
        inProducts[i]['details'] = prod['details']
        inProducts[i]['productId'] = prod['id']
        inProducts[i]['productPrice'] = prod['pr']
        totalPrice += prod['pr']
        inProducts[i]['count'] = prod['count']

    try:
        for i in range(len(inProducts)):
            cursor.execute("insert into orders_to_products (\"order_ID\", \"product_ID\", amount) values ({orderId}, {inProducts[i]['productId']}, {inProducts[i]['count']})")
        productsAddedFlag = True
        print('products added')
    except:
        productsAddedFlag = False
        print('products were not added')

    outData = {}

    if productsAddedFlag == True and orderAddedFlag == True:
        outData['addedFlag'] = True
    else:
        outData['addedFlag'] = False

    return json.dumps(outData)



@app.route("/productsToOrder", methods=["POST"])
def insertProductsToBuy():
    cursor = conn.cursor()
    jsonInData = json.loads(request.get_data())
    inDataCategory = jsonInData["productName"]
    inDataDetails = jsonInData["productDetails"]
    inDataAmount = jsonInData["productAmount"]

    categoriesFromDb = cursor.execute("select * from products_categories")
    categoriesFromDb = cursor.fetchall()
    categories = {}
    for i in range(len(categoriesFromDb)):
        categories[categoriesFromDb[i][1]] = categoriesFromDb[i][0]

    productId = cursor.execute("select id from products where category = '{0}' and details = '{1}'".format(
            categories[inDataCategory], inDataDetails
        ))
    productId = cursor.fetchall()
    
    dataToDb = {}
    dataToDb["productId"] = productId
    dataToDb["amount"] = inDataAmount
    
    outData = {}

    isOrderInDbFromDb = cursor.execute('select * from products_to_buy where "product_ID" = {0}'.format(productId))
    isOrderInDbFromDb = cursor.fetchall()
    try:
        if isOrderInDbFromDb is None:
            cursor.execute("insert into products_to_buy (\"product_ID\", amount) values ({0}, {1})".format(productId, inDataAmount))
        else:
            cursor.execute("update products_to_buy set amount = {0} where id = {1}".format(
                isOrderInDbFromDb[2] + inDataAmount, id = isOrderInDbFromDb[0]
            ))
        outData['addedFlag'] = True
        print('i ran')
    except:
        outData['addedFlag'] = False
        print('i didnt run')

    return json.dumps(outData)


#conn.close()
if __name__ == '__main__':
    #app = Flask(__name__, template_folder='../pages', static_folder='../pages')
    app.run(debug=True, host="127.0.0.1")
    addOrderToDb()