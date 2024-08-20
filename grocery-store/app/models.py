'''database model for grocery app where the database will contain 6 tables
1.admin
2.users
3.catogories
4.products
5.orders
6.cart
''' 

from app import app,db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

#######################################################################

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model,UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    hashed_password = db.Column(db.String(255))
    role=db.Column(db.Text)
    
    def __init__(self,name,email,password,role):
        self.name=name
        self.email=email
        self.hashed_password=generate_password_hash(password)
        self.role=role
        
    def check_password(self,password):
        return check_password_hash(self.hashed_password,password)
    
    def get_id(self):
        return (self.user_id)
    

#######################################################################

class Category(db.Model):
    
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    
    def __init__(self,name):
        self.name=name
        
    def to_dict(self):
        return {'name':self.name}

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255),index=True)
    quantity_avail = db.Column(db.Float)
    unit = db.Column(db.String(255))
    price_per_unit = db.Column(db.Float)
    expiry = db.Column(db.DateTime)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.cat_id'))
    
    def __init__(self,name,quantity_avail,unit,price_per_unit,expiry,cat_id):
        self.name=name
        self.quantity_avail=quantity_avail
        self.unit=unit
        self.price_per_unit=price_per_unit
        self.expiry=expiry
        self.cat_id=cat_id
    
    #this function would be useful for API CRUD operations    
    def to_dict(self):
        return {
            'name': self.name,
            'quantity_avail': self.quantity_avail,
            'unit': self.unit,
            'price_per_unit': self.price_per_unit,
            'expiry': self.expiry,
            'cat_id': self.cat_id
        }

class Order(db.Model):
    order_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    subprice = db.Column(db.Float)
    date = db.Column(db.DateTime)
    discount = db.Column(db.Float)
    shipping = db.Column(db.Integer)
    total = db.Column(db.Float)
    status=db.Column(db.String(50))
    
    def __init__(self,order_id,user_id,subprice,date,discount,shipping,total,status):
        self.order_id=order_id
        self.user_id=user_id
        self.subprice=subprice
        self.date=date
        self.discount=discount
        self.shipping=shipping
        self.total=total
        self.status=status

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    order_id = db.Column(db.String(255))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    qty= db.Column(db.Float)
    price = db.Column(db.Float)
    
    def __init__(self,user_id,order_id,product_id,qty,price):
        self.user_id=user_id
        self.order_id=order_id
        self.product_id=product_id
        self.qty=qty
        self.price=price
        
        

        




