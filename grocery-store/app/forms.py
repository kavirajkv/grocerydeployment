#forms for every user and admin functionality

from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField,IntegerField,PasswordField,DateField
from wtforms.validators import DataRequired,Email,NumberRange,EqualTo,Length



###################################################################################
#login form for admin
  
class adminlogin(FlaskForm):
    email=StringField('Enter your registered email: ',validators=[DataRequired(),Email()])
    password=PasswordField('Enter your password: ',validators=[DataRequired()])
    login=SubmitField('Log in')
    
###################################################################################    
#registraion for users and admin

class Usersregistration(FlaskForm):
    name=StringField('Enter your name: ',validators=[DataRequired()])
    email=StringField('Enter your email: ',validators=[DataRequired(),Email()],render_kw={'placeholder':'abc@xyzmail.com'})
    password=PasswordField('Password: ',validators=[DataRequired(),Length(min=8),EqualTo('pass_confirm',message='Passwords must match')],render_kw={'placeholder':'Min 8 charcters'})
    pass_confirm=PasswordField('Confirm password: ',validators=[DataRequired()])
    role=SelectField('Please select your role: ',choices=[('User','User'),('Admin','Admin')],validators=[DataRequired()])
    register=SubmitField('Register')

#####################################################################    
#login for users 
class Userslogin(FlaskForm):
    email=StringField('Enter your registered email: ',validators=[DataRequired(),Email()])
    password=PasswordField('Enter your password: ',validators=[DataRequired()])
    login=SubmitField('Log in')
    
    
#########################################################################################
#forms for admin to do CRUD operations in the inventry

class addcategory(FlaskForm):
    name=StringField('Enter the name of the category: ',validators=[DataRequired()])
    add=SubmitField('Add category')
 

class deletecategory(FlaskForm):
    name=StringField('Enter the name of the category to delete: ',validators=[DataRequired()])
    delete=SubmitField('Delete category')
    
class addproduct(FlaskForm):
    name=StringField('Enter the name of the product: ',validators=[DataRequired()])
    quantity=IntegerField('Enter the no.of quantity to be added: ',validators=[DataRequired(),NumberRange(min=0)])
    unit=SelectField('Enter the measuring unit of the product: ',choices=[("kg",'kg'),("litre","litre"),("Each","Each")],validators=[DataRequired()])
    priceperunit=IntegerField('Enter the price per unit: ',validators=[DataRequired(),NumberRange(min=0)])
    expiry=DateField('Enter the expiry date: ',validators=[DataRequired()])
    category=StringField('Enter the category: ',validators=[DataRequired()])
    submit=SubmitField('Submit')
    
class updateproduct(FlaskForm):
    name=StringField('Enter the name of the product to update: ',validators=[DataRequired()])
    quantity=IntegerField('Enter the no.of quantity to be added or remove: ',validators=[DataRequired(),NumberRange(min=0)])
    priceperunit=IntegerField('Enter the price to be updated: ',validators=[DataRequired(),NumberRange(min=0)])
    submit=SubmitField('Submit')
    
class deleteproduct(FlaskForm):
    name=StringField('Enter the name of the product to delete: ',validators=[DataRequired()])
    submit=SubmitField('Submit')    
 
##############################################
'''search feature form'''

class usersearchproduct(FlaskForm):
    name=StringField('Enter any product name: ',render_kw={'placeholder':'Search products'}) 
    submit=SubmitField('Search')

#############################################################################################
#user operation with cart

class addtocart(FlaskForm):
    quantity=IntegerField('Enter valid amount of quantity to add: ',validators=[DataRequired(),NumberRange(min=1)])
    submit=SubmitField('Add')
    
#form to edit the cart
    
class Editcart(FlaskForm):
    quantity=IntegerField('Enter the amount of quantity to edit: ',validators=[DataRequired(),NumberRange(min=1)])
    submit=SubmitField('Edit')