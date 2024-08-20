from app import app, db
from app.models import Category, Product
from flask import request,jsonify
from datetime import datetime


##########################################################################################
'''REST API implementation for CRUD operations in category and product table'''
####################################
#REST API for crud operations in category table

#for getting category names
@app.route('/api/category', methods=['GET'])
def get_category():
    with app.app_context():
        categories=Category.query.all()
    
    categories_list = [category.to_dict() for category in categories]
    return jsonify(categories_list)


#for adding category name
@app.route('/api/category', methods=['POST'])
def add_category():
    category_data = request.json
    name = category_data.get('name')
    category = Category(name=name)
    with app.app_context():
        category_to_search = Category.query.filter(Category.name.ilike(name)).first()
        if category_to_search:
            return jsonify({'message':'category already found'}),409
        else:
            db.session.add(category)
            db.session.commit()
        return jsonify({'message': 'Category added successfully'})


#for removing a category from category table this will eventually delete all products associated with it 
@app.route('/api/category/', methods=['DELETE'])
def delete_category():
    del_category=request.json
    name=del_category.get('name')
    with app.app_context():
        category = Category.query.filter(Category.name.ilike(name)).first()
        if category:
            products_to_del=Product.query.filter_by(cat_id=category.cat_id).all()
            if products_to_del:
                for product in products_to_del:
                    db.session.delete(product)
            db.session.delete(category)
            db.session.commit()
            return jsonify({'message': 'Category and all products associated with it are deleted successfully'})

    return jsonify({'message': 'Category not found'}), 404

###########################################
#REST API for crud operations in products table:
'''----operations that would be handled by API----
-Add a new product -admin
-Update a product -admin 
-Remove a product -admin
-Read products of specific category
-Search a specific product

'''

#Adding a new product
@app.route('/api/product',methods=['POST'])
def add_product():
    product=request.json
    name=product.get('name')
    qavail=product.get('qavail')
    unit=product.get('unit')
    price=product.get('price')
    expiry=product.get('expiry')
    category_name=product.get('category_name')
    
    with app.app_context():
        category=Category.query.filter_by(name=category_name).first()
        
        if category:
            expiry_date = datetime.strptime(expiry, '%d-%m-%Y').date()
            product_toadd=Product(name=name,quantity_avail=qavail,unit=unit,price_per_unit=price,expiry=expiry_date,cat_id=category.cat_id)
            db.session.add(product_toadd)
            db.session.commit()
            return jsonify({'message':'product added successfully'})
        else:
            return jsonify({'message':'category not found'}),404
            
    
    
#for getting all products   
@app.route('/api/product',methods=['GET'])
def read_product():
    with app.app_context():
        products=Product.query.all()
        
    products_list=[product.to_dict() for product in products ]
    return jsonify(products_list)

#for removing a product
@app.route('/api/product',methods=['DELETE'])
def delete_product():
    delete_product=request.json
    name=delete_product.get('name')
    
    with app.app_context():
        product_todel=Product.query.filter(Product.name.ilike(name)).first()
        if product_todel:
            db.session.delete(product_todel)
            db.session.commit()
            return jsonify({'message':'product deleted'})
        return jsonify({'message':'product not found'}),404
    
    
#for updating the product
@app.route('/api/product',methods=['PATCH'])
def update_product():
    update=request.json
    name=update.get('name')
    quantity=update.get('quantity')
    price=update.get('price')
    
    with app.app_context():
        product=Product.query.filter(Product.name.ilike(name)).first()
        if product:
            product.quantity_avail=quantity
            product.price_per_unit=price
            db.session.commit()
            return jsonify({'message':'product updated successfully'})
        return jsonify({'message':'product not found'}),404
            
#for getting products of specific category
@app.route('/api/product_of_cat',methods=['GET'])
def productsofcategory():
    categorytoget=request.json
    category_name=categorytoget.get('category_name')
    with app.app_context():
        category=Category.query.filter_by(name=category_name).first()
        if category:
            products=Product.query.filter_by(cat_id=category.cat_id).all()
            if products:
                productslist=[{'id':product.product_id,'name':product.name,'quantity':product.quantity_avail,'price':product.price_per_unit,'expiry':product.expiry} for product in products]
                return jsonify(productslist)
        return jsonify({'message':'category not found'}),404

#for getting products using product name (can be used as a search functionality) and also add to cart functionality
@app.route('/api/searchproduct',methods=['GET'])
def searchproduct():
    product_to_search=request.json
    product_name=product_to_search.get('product_name')
    
    with app.app_context():
        products=Product.query.filter(Product.name.ilike(f'%{product_name}%')).all()
        if products:
            productslist=[{'id':product.product_id,'name':product.name,'quantity':product.quantity_avail,'price':product.price_per_unit,'expiry':product.expiry} for product in products]
            return jsonify(productslist)
        return jsonify({'message':'product not found'}),404
    
    
#for getting product of each category
@app.route('/api/product_of_eachcategory',methods=['GET'])
def product_of_each_category():
    with app.app_context():
        categories=Category.query.all()
        productslist={}
        for category in categories:
            products=Product.query.filter_by(cat_id=category.cat_id).all()
            if products:
                productlist=[{'id':product.product_id,'name':product.name,'quantity':product.quantity_avail,'price':product.price_per_unit,'expiry':product.expiry} for product in products]
                productslist[category.name]=productlist
        return jsonify(productslist)

    