class Config:
    username = 'ekaterina'
    password = 'pass'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{username}:{password}@localhost/memento_mori'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 
    CSRF_ENABLED = True
    SECRET_KEY = 'no_time_to_die'