#views of grocery store application which controls the CRUD operation through api and login controls


from app import app, db
from app.models import Users, Product, Order, Cart
from app.forms import adminlogin, addcategory, Usersregistration, Userslogin, deletecategory, addproduct, updateproduct, deleteproduct, addtocart,usersearchproduct,Editcart
from flask import render_template,redirect, url_for, flash,get_flashed_messages
import requests,uuid
from datetime import datetime
from flask_login import login_user,logout_user,login_required,current_user
    
    
###################################################################################
'''Views and feature to be routed for the grocery store app'''

#first page when user/admin landed
@app.route('/')
def index():
    messages=get_flashed_messages()
    return render_template('index.html',messages=messages)



################################
'''USER and ADMIN registration'''

@app.route('/userregistration',methods=['GET','POST'])
def userregister():
    form=Usersregistration()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        user=Users(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data,
                    role=form.role.data)
        with app.app_context():
            checkuser=Users.query.filter_by(email=form.email.data).first()
            if checkuser:
                flash('your email already registered please login')
                return redirect(url_for('userloginpage'))
            else:
                db.session.add(user)
                db.session.commit()
                flash('you are registered successfully! kindly login to continue')
                return redirect(url_for('index'))
    return render_template('userlogin/user_registration.html',form=form,messages=messages)

#############################################################################
'''ADMIN login'''

@app.route('/adminlogin',methods=['GET','POST'])
def adminloginpage():
    form=adminlogin()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        with app.app_context():
            admin=Users.query.filter_by(email=form.email.data).first()
            if admin is None:
                flash('You are not an admin please register to login')
                return redirect(url_for('adminloginpage')) 
            if admin is not None and admin.check_password(form.password.data) and admin.role=='Admin':
                login_user(admin)
                return redirect(url_for('adminhome'))
            else:
                flash ('please check your email or password or you may not be an admin')
                return redirect(url_for('adminloginpage'))
    return render_template('adminlogin/admin_login.html',form=form,messages=messages)


########################################################
'''USER login'''
@app.route('/userlogin',methods=['GET','POST'])
def userloginpage():
    form=Userslogin()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        with app.app_context():
            user=Users.query.filter_by(email=form.email.data).first()
            if user is None:
                flash('You are not an user please register to login')
                return redirect(url_for('userloginpage'))   
            elif user is not None and user.check_password(form.password.data) and user.role=='User':
                login_user(user)
                return redirect(url_for('userhome'))
            else:
                flash ('please check your email or password')
                return redirect(url_for('userloginpage'))
    return render_template('userlogin/user_login.html',form=form,messages=messages)

#########################################################
#common logout functionality for both admin and user           
@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

######################################################################################
'''ADMIN views'''

#admin's homepage
@login_required
@app.route('/admin')
def adminhome():
    return render_template('admin/adminhome.html')

#view for admin to add category using add category api 
@app.route('/addcategory',methods=['GET','POST'] )
def categoryadd():
    form=addcategory()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        category_name=form.name.data
        payload={"name":category_name}
        url='http://localhost:5000/api/category'
        response=requests.post(url,json=payload)
        if response.status_code==200:
            flash ('category added successfully','success')
        elif response.status_code==409:
            flash ('Category already found','info')
        else:
            flash ('category not added','error')
        return redirect(url_for('categoryadd'))
        
    return render_template('admin/addcategory.html',form=form,messages=messages)  


#view for admin to list categories using api through get request
@app.route('/listcategory',methods=['GET'])
def categorylist():
    url='http://localhost:5000/api/category'
    response=requests.get(url)
    if response.status_code==200:
        categories=response.json()
        return render_template('admin/listcategory.html',categories=categories)
    else:
        return 'Error occured on fetching category'
    
    
#view for admin to delete a category
@app.route('/deletecategory',methods=['GET','DELETE','POST'])
def categorydelete():
    form=deletecategory()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        category_name=form.name.data
        payload={"name":category_name}
        url='http://localhost:5000/api/category'
        response=requests.delete(url,json=payload)
        if response.status_code==200:
            flash ('Category and products associated with it are deleted','success')
        else:
            flash('Category not found','error')
        return redirect(url_for('categorydelete'))
    
    return render_template('admin/deletecategory.html',form=form,messages=messages)
    
    
#view for admin to list all the available product
@app.route('/listproducts',methods=['GET'])
def listproducts():
    url='http://localhost:5000/api/product'
    response=requests.get(url)
    if response.status_code==200:
        products=response.json()
        return render_template('admin/listproduct.html',products=products)
    else:
        return 'Error fetching products'

       
#view for admin to add a product
@app.route('/addproduct',methods=['GET','POST'])
def productadd():
    form=addproduct()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        product_name=form.name.data
        product_quantity=form.quantity.data
        product_unit=form.unit.data
        product_price=form.priceperunit.data
        product_expiry=form.expiry.data.strftime("%d-%m-%Y")
        product_category=form.category.data
        
        payload={"name":product_name,
                "qavail":product_quantity,
                "unit":product_unit,
                "price":product_price,
                "expiry":product_expiry,
                "category_name":product_category}
        url='http://localhost:5000/api/product'
        response=requests.post(url,json=payload)
        if response.status_code==200:
            flash ('Product added successfully','success')
        else:
            flash ('Product addition failed please try again with correct data','error') 
        return redirect(url_for('productadd')) 
    return render_template('admin/addproduct.html',form=form,messages=messages)

#view for admin to delete a product
@app.route('/deleteproduct',methods=['GET','POST','DELETE'])
def productdelete():
    form=deleteproduct()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        product_name=form.name.data
        payload={"name":product_name} 
        url='http://localhost:5000/api/product'
        response=requests.delete(url,json=payload)  
        if response.status_code==200:
            flash ('product deleted sucessfully','success')
        else:
            flash ('product deletion unsucessful please check the name again','error')
        return redirect(url_for('productdelete'))
    return render_template('admin/deleteproduct.html',form=form,messages=messages)      

#view for admin to update a product
@app.route('/updateproduct',methods=['GET','POST','PATCH'])
def productupdate():
    form=updateproduct()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        product_name=form.name.data
        product_quantity=form.quantity.data
        product_price=form.priceperunit.data
        payload={"name":product_name,
                "quantity":product_quantity,
                "price":product_price}
        url='http://localhost:5000/api/product'
        response=requests.patch(url,json=payload)
        if response.status_code==200:
            flash ('Product updated','success')
        else:
            flash ('Please check the product name','error')
        return redirect(url_for('productupdate'))
    return render_template('admin/updateproduct.html',form=form,messages=messages)



####################################################################################
'''USER views'''

@login_required
@app.route('/user')
def userhome():
    messages=get_flashed_messages()
    return render_template('users/userhome.html',messages=messages)

#view for user to get products of each category
@app.route('/products',methods=['GET'])
def userproductlist():
    url='http://localhost:5000/api/product_of_eachcategory'
    response=requests.get(url)
    if response.status_code==200:
        categories=response.json()
        return render_template('users/userproductlist.html',categories=categories)
    return 'error fetching products'


#view for user to search for an item
@app.route('/searchproduct',methods=['GET','POST'])
def usersearch():
    form=usersearchproduct()
    messages=get_flashed_messages()
    if form.validate_on_submit():
        product_name=form.name.data
        payload={"product_name":product_name}
        url='http://localhost:5000/api/searchproduct'
        response=requests.get(url,json=payload)
        if response.status_code==200:
            products=response.json()
            return render_template('users/searchproduct.html',products=products)
        else:
            flash ('Product not found')
        return redirect(url_for('usersearch'))
    return render_template('users/usersearch.html',form=form,messages=messages)
            
            
#view for user to add a product to cart 
@app.route('/addtocart/<string:productname>',methods=['GET','POST'])  
def add_to_cart(productname):
    form=addtocart()
    messages=get_flashed_messages()
    payload={"product_name":productname}
    url='http://localhost:5000/api/searchproduct'
    response=requests.get(url,json=payload)
    if response.status_code==200:
        product=response.json()
    else:
        return 'product not found'
    if form.validate_on_submit():
        quantity=form.quantity.data
        if quantity>product[0]["quantity"]:
            flash("Please don't enter quantity more than available")
            return redirect(url_for('add_to_cart',productname=product[0]["name"]))
        userid=current_user.user_id
        productid=product[0]["id"]
        subprice=product[0]["price"]*int(quantity)
        cartitem=Cart(user_id=userid,order_id='abc',product_id=productid,qty=quantity,price=subprice)
        with app.app_context():
            db.session.add(cartitem)
            db.session.commit()
            flash('Product added to cart')
            return redirect(url_for('userhome'))
    return render_template('users/addtocart.html',form=form,messages=messages,product=product)

#view for cart functionality
@app.route('/cart',methods=['GET','POST'])
def cart():
    userid=current_user.user_id
    with app.app_context():
        cartitems=Cart.query.filter_by(user_id=userid).all()
        if cartitems:
            total_price = sum(cart_item.price for cart_item in cartitems)
            return render_template('users/cart.html',cartitems=cartitems,getproductname=getproductname,total_price=total_price)
        else:
            return render_template('users/cart.html',cartitems=None,total_price=0)
              
#helper function for cart function to get product name from id
def getproductname(productid):
    product=Product.query.get(productid)   
    if product:
        return product.name
    else:
        return 'unknown'        
    
#functionality for user can remove any product from cart
@app.route('/removefromcart/<string:cart_id>',methods=['GET','POST'])
def removefromcart(cart_id):
    with app.app_context():
        remove=Cart.query.get(cart_id)
        if remove:
            db.session.delete(remove)
            db.session.commit()
            return redirect(url_for('cart'))
        
#functionality for user to edit the cart
@app.route('/editcart/<string:cart_id>',methods=['GET','POST'])
def editcart(cart_id):
    form=Editcart()
    messages=get_flashed_messages()
    qunatitytoedit=form.quantity.data
    if form.validate_on_submit():
        with app.app_context():
            cartitem=Cart.query.filter_by(cart_id=cart_id).first()
            if cartitem:
                oldprice=cartitem.price
                oldqty=cartitem.qty
                price=oldprice/oldqty
                newprice=qunatitytoedit*price
                cartitem.qty=qunatitytoedit
                cartitem.price=newprice
                productqty=Product.query.filter_by(product_id=cartitem.product_id).first()
                if productqty:
                    if productqty.quantity_avail<qunatitytoedit:
                        flash("Please don't order above quantity available")
                        return redirect(url_for('editcart',cart_id=cart_id))
                db.session.commit()
                return redirect(url_for('cart'))
    return render_template('users/editcart.html',form=form,messages=messages)


#functionality to make order from cart
@app.route('/makeorder',methods=['GET','POST'])
def makeorder():
    userid=current_user.user_id
    with app.app_context():
        cartitems=Cart.query.filter_by(user_id=userid).all()
        if cartitems: 
            id=uuid.uuid1()
            orderid=id.hex
            for item in cartitems:
                item.order_id=orderid
            db.session.commit()
            total_price = sum(cart_item.price for cart_item in cartitems)
            currentdate=datetime.now()
            discount_eligible=Order.query.filter_by(user_id=userid).first()
            if discount_eligible:
                discount=0
            else:
                discount= total_price - (total_price - (total_price*(25/100)))
            shipping=40
            total=float((total_price+shipping)-discount)
            orderitems=Order(order_id=orderid,user_id=userid,subprice=total_price,date=currentdate,discount=discount,shipping=shipping,total=total,status='No action')
            db.session.add(orderitems)
            db.session.commit()
    return render_template('users/order.html',total_price=total_price,discount=discount,shipping=shipping,total=total,orderid=orderid)


#funnctionality to make successful order and it will eventually decrease the quantity available of the products
@app.route('/makepayment/<string:orderedid>',methods=['GET','POST'])
def makepayment(orderedid):
    with app.app_context():
        paymentorder=Order.query.filter_by(order_id=orderedid).first()
        if paymentorder:
            paymentorder.status='Ordered'
            db.session.commit()
        cartproduct=Cart.query.filter_by(order_id=orderedid).all()
        if cartproduct:
            for product in cartproduct:
                orderedproduct=product.product_id
                orderedquantity=product.qty
                changeproduct=Product.query.filter_by(product_id=orderedproduct).first()
                if changeproduct:
                    newquantity=changeproduct.quantity_avail-orderedquantity
                    changeproduct.quantity_avail=newquantity
                    db.session.commit()
        return render_template('users/thankyou.html')
    
#functionality to cancel the order
@app.route('/cancelorder/<string:orderedid>',methods=['GET','POST'])
def cancelorder(orderedid):
    with app.app_context():
        ordertocancel=Order.query.filter_by(order_id=orderedid).first()
        if ordertocancel:
            ordertocancel.status='Cancelled'
            db.session.commit()
            return redirect(url_for('userhome'))
        
#functionality to list orders to user
@app.route('/orderslist',methods=['GET','POST']) 
def getorders():   
    with app.app_context():
        userid=current_user.user_id
        orders=Order.query.filter_by(user_id=userid).all()
        if orders:
            return render_template('users/orderslist.html',orders=orders)
        else:
            return render_template('users/orderslist.html',orders=None)
            