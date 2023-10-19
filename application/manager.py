from flask import render_template, request, session,redirect,url_for, flash, json
from flask import current_app as app
from application.database import *
from datetime import datetime
from sqlalchemy import or_

def search(search_query):
    search_results = Product.query.filter(
        or_(Product.name.ilike(f'%{search_query}%'),
                Product.description.ilike(f'%{search_query}%'),
                Product.price.ilike(f'%{search_query}%'),
                Product.mgf_date.ilike(f'%{search_query}%'),
                Product.exp_date.ilike(f'%{search_query}%'))
    ).all()
    return search_results

@app.route('/manager', methods=['POST','GET'])
def manager_page():
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            coupons = Coupon.query.all()
            print(coupons, "printed coupon")
            search_query = request.args.get('search_query')
            if search_query:
                categories = Category.query.all()
                products = search(search_query)
                return render_template('manager_page.html', products=products, categories=categories, coupons=coupons)
            else:
                products = Product.query.all()
                categories = Category.query.all()
            return render_template('manager_page.html', products=products, categories=categories, coupons=coupons)
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/category', methods=['POST','GET'])
def create_category():
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            if request.method=='POST':
                name = request.form.get('name')
                new_category = Category(name=name)
                db.session.add(new_category)
                db.session.commit()
                flash("Category added successfully.")
                return redirect(url_for('manager_page'))
            else:
                return render_template('category.html', mode="add")
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/manager/category/<int:category_id>', methods=['GET', 'POST'])
def get_category(category_id):
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            if request.method=='POST':
                category = Category.query.filter_by(id=category_id).first()
                name = request.form.get('name')
                category.name=name
                db.session.commit()
                flash("Category added successfully")
                return redirect(url_for('manager_page'))
            else:
                category = Category.query.filter_by(id=category_id).first()
                return render_template('category.html', category=category, mode="update")
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/category/delete/<int:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            if request.method=='POST':
                category = Category.query.filter_by(id=category_id).first()
                for product in category.products:
                    db.session.delete(product)
                    db.session.commit()
                db.session.delete(category)
                db.session.commit()
                flash("Category deleted successfully.")
                return redirect(url_for('manager_page'))
            else:
                category = Category.query.filter_by(id=category_id).first()
                return render_template('category.html', category=category, mode="delete")
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/products', methods=['POST', 'GET'])
def create_product():
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            if request.method=='POST':
                format="%Y-%m-%d"
                name = request.form.get('name')
                description = request.form.get('description')
                price = request.form.get('price')
                mgf_date = datetime.strptime(request.form.get('mgf_date'),format)
                exp_date = datetime.strptime(request.form.get('exp_date'),format)
                stock = request.form.get('stock')
                img_name = request.form.get('img_name')
                category_id = request.form.get('category_id')
                print(category_id)
                new_product = Product(name=name, description=description, price=price, mgf_date=mgf_date, exp_date=exp_date, stock=stock, category_id=category_id, img_name=img_name)
                db.session.add(new_product)
                db.session.commit()
                flash("Product added successfully")
                return redirect(url_for('manager_page'))
            else:
                categories = Category.query.all()
                return render_template('product.html', categories=categories, mode="add")
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/products/<int:product_id>', methods=['GET', 'POST'])
def get_product(product_id):
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            if request.method=='POST':
                product = Product.query.filter_by(id=product_id).first()
                format="%Y-%m-%d"
                product.name = request.form.get('name')
                product.description = request.form.get('description')
                product.price = request.form.get('price')
                product.mgf_date = datetime.strptime(request.form.get('mgf_date'),format)
                product.exp_date = datetime.strptime(request.form.get('exp_date'),format)
                product.stock = request.form.get('stock')
                product.category_id = request.form.get('category_id')
                product.img_name = request.form.get('img_name')
                db.session.commit()
                flash("Product updated successful.")
                return redirect(url_for('manager_page'))
            else:
                categories = Category.query.all()
                product = Product.query.filter_by(id=product_id).first()
                return render_template('product.html', product=product, mode="update", categories=categories)
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
@app.route('/products/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            if request.method=='POST':
                product = Product.query.filter_by(id=product_id).first()
                db.session.delete(product)
                db.session.commit()
                flash("Product added successfully.")
                return redirect(url_for('manager_page'))
            else:
                product = Product.query.filter_by(id=product_id).first()
                return render_template('product.html', product=product, mode="delete")
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')


@app.route('/manager/create/coupon', methods=['POST', 'GET'])
def create_coupon():
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            if request.method=='POST':
                code=request.form.get('code')
                type=request.form.get('type')
                value=request.form.get('value')
                coupon = Coupon(code=code, type=type, value=int(value))
                db.session.add(coupon)
                db.session.commit()
                flash("Coupon created.")
                return redirect(url_for('manager_page'))
            else:
                return render_template('coupon.html')
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/manager/delete/coupon/<int:id>', methods=['POST', 'GET'])
def delete_coupon(id):
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            coupon = Coupon.query.get(id)
            db.session.delete(coupon)
            db.session.commit()
            flash("Coupon Deleted.")
            return redirect(url_for('manager_page'))
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
