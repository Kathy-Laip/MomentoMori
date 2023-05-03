# # from flask import Flask, request, render_template
# # import sqlalchemy
# # from config import Config
# # import numpy as np
# # import json

# # class Connection:
# #     def __init__(self, db):
# #         self.db = db
    
# #     def get_data_from_table(self, query):
# #         connection = self.db.connect()
# #         return np.array(connection.execute(query).fetchall())

# #     def execute_query(self, query):
# #         connection = self.db.connect()
# #         connection.execute(query)

# # app = Flask(__name__, template_folder='./pages', static_folder='./pages')
# # app.config.from_object(Config)
# # my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
# # connection = Connection(my_db)

# # data = connection.get_data_from_table("select * from orders")

# # print(data)

# # if __name__ == '__main__':
# #     app.run(debug=True, host="127.0.0.1")

# import psycopg2
# from flask import Flask, redirect, url_for, render_template, request
# import json
# from config import Config
# import numpy as np
# from configparser import ConfigParser


# def config(filename='database.ini', section='postgresql'):
#     parser = ConfigParser()
#     parser.read(filename)

#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))
#     return db

# def connect():
#     conn = None
#     try:
#         params = config()
#         print('Connecting to the PostgreSQL database...')
#         print(params)
#         conn = psycopg2.connect(**params)
#         cur = conn.cursor()
        
#         print('PostgreSQL database version:')
#         cur.execute('SELECT version()')

#         db_version = cur.fetchone()
#         print(db_version)
        
#         cur.close()
#     except (Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
#         print("error")
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')
#         else:
#             print('Database connection failed for some reason')


# if __name__ == '__main__':
#     app = Flask(__name__, template_folder='./pages', static_folder='./pages')
#     connection = connect()
#     # cursor = connection.cursor()