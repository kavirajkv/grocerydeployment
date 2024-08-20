#__init__ file where app initialization and configuration scripts are managed


##########################################################

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


########################################################

#initializing flask application
app=Flask(__name__)
login_manager=LoginManager()

pgsql_user=os.environ.get('POSTGRES_USER')
pgsql_password=os.environ.get('POSTGRES_PASSWORD')
datapath=os.environ.get('url')

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{pgsql_user}:{pgsql_password}@{datapath}:5432/testdata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#database connectivity through ORM
db = SQLAlchemy(app)

Migrate(app,db) #for retaining data even if schema changes occur

login_manager.init_app(app)
login_manager.login_view='login'

#importing models for the database and creation of database


from app.models import  Users, Category, Product, Order, Cart

with app.app_context():
    db.create_all()


from app import views

from app import api
