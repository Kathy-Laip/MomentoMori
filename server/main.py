import psycopg2
from flask import Flask, redirect, url_for, render_template, request
import json


app = Flask(__name__)
connection = psycopg2.connect(
    database="memento_mori", user="postgres", password="password", host="127.0.0.1", port="5433"
)
cursor = connection.cursor()


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
    app.run(debug=True)