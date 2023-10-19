from flask import render_template, request, session,redirect,url_for, flash
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

@app.route('/user', methods=['POST','GET'])
def user_page():
    if session.get('current_user'):
        if session['current_user']['role']=='user':
            search_query = request.args.get('search_query')
            products=None
            if search_query:
                products = search(search_query)
            else:
                products = Product.query.all() 
            categories = Category.query.all()
            if session.get('session_cart'):
                cart=len(session['session_cart'])
            else:
                cart=0
            mode="all"
            current_url='/user'
            return render_template('user_page.html', products=products, categories=categories, cart=cart, mode=mode, current_url=current_url)
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/user/category/<int:category_id>', methods=['POST','GET'])
def user_page_by_category(category_id):
    if session.get('current_user'):
        if session['current_user']['role']=='user':
            search_query = request.args.get('search_query')
            products=None
            if search_query:
                products = search(search_query)
            else:
                products = Product.query.filter_by(category_id=category_id).all()
            category = Category.query.filter_by(id=category_id).first()
            if session.get('session_cart'):
                cart=len(session['session_cart'])
            else:
                cart=0
            if session.get('session_cart'):
                cart=len(session['session_cart'])
            else:
                cart=0
            mode="one"
            current_url='/user/category/'+ str(category.id)
            return render_template('user_page.html', products=products, category=category, cart=cart, mode=mode, current_url=current_url)
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/user/session/cart/activated', methods=['POST','GET'])
def sessioon_cart_activate():
    if session.get('current_user'):
        if session['current_user']['role']=='user':
            if request.method=='POST':
                current_url = request.form.get('current_url')
                product_id = request.form.get('product_id')
                if 'session_cart' not in session:
                    session['session_cart'] = []

                session['session_cart'].append(product_id)
                session.modified = True
                flash("Product added successfully")
            return redirect(current_url)
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/user/mycart')
def mycart():
    if session.get('current_user'):
        if session['current_user']['role']=='user':
            session_cart=session['session_cart']
            products={}
            total=0
            for product_id in session_cart:
                product=Product.query.filter_by(id=product_id).first()
                if product_id not in products.keys():
                    products[product_id]=[product.name,1, product.price]
                else:
                    if product.stock> products[product_id][1]:
                        products[product_id][1]+=1
                    else:
                        products[product_id][1]=product.stock
            for product in products.keys():
                total+=products[product][1]*products[product][2]
            coupons = Coupon.query.all()
            return render_template('mycart.html', products=products, total=total, coupons=coupons)
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/user/checkout', methods=['POST'])
def checkout():
    if session.get('current_user'):
        if session['current_user']['role']=='user':
            selected_items = request.form.getlist('Qty')
            coupon_id = request.form.get('is_coupon_id')
            if coupon_id=="Select Coupon":
                coupon_id=None
            saved_amount = 0
            coupon=None
            if coupon_id:
                coupon = Coupon.query.get(int(coupon_id))
            for each_item in selected_items:
                product_ids = each_item.split('_')
                product = Product.query.filter_by(id=int(product_ids[1])).first()
                product_name=product.name
                category = Category.query.filter_by(id=product.category_id).first()
                category_name = category.name
                quantity = int(product_ids[0])
                user = User.query.filter_by(username=session['current_user']['username']).first()
                user_id = user.id
                if coupon:
                    if coupon.type=='flat':
                        amount = product.price * int(product_ids[0]) - coupon.value
                        saved_amount += coupon.value
                        order=Order(product_name=product_name, category_name=category_name, amount=amount, quantity=quantity, user_id=user_id)
                        db.session.add(order)
                        db.session.commit()
                        product.stock-=int(product_ids[0])
                        db.session.commit()
                    elif coupon.type=='discount':
                        amount = product.price * int(product_ids[0]) - (product.price * int(product_ids[0]))*(coupon.value/100)
                        saved_amount += (product.price * int(product_ids[0]))*(coupon.value/100)
                        order=Order(product_name=product_name, category_name=category_name, amount=amount, quantity=quantity, user_id=user_id)
                        db.session.add(order)
                        db.session.commit()
                        product.stock-=int(product_ids[0])
                        db.session.commit()
                else:
                    amount = product.price * int(product_ids[0])
                    order=Order(product_name=product_name, category_name=category_name, amount=amount, quantity=quantity, user_id=user_id)
                    db.session.add(order)
                    db.session.commit()
                    product.stock-=int(product_ids[0])
                    db.session.commit()
            session['session_cart'].clear()          
            if saved_amount > 0:
                saved_amount=format(saved_amount,'0.2f')
                flash(f"Purchase successful! You saved {saved_amount} on this purchase. with the coupon {coupon.code}")
                return redirect(url_for('user_page'))
            else:
                flash(f"Purchase successful!")
                return redirect(url_for('user_page'))
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/remove/item/<string:key>')
def remove_item(key):
    if session.get('current_user'):
        if session['current_user']['role']=='user':
            session_cart=session['session_cart']
            print(session_cart)
            session_cart_set = set(session_cart)
            print(session_cart_set)
            session_cart=list(session_cart_set)
            print(session_cart)
            session_cart.remove(key)
            session['session_cart']=session_cart
            return redirect(url_for('mycart'))
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/user/cancel/checkout')
def checkout_cancel():
    if session.get('current_user'):
        if session['current_user']['role']=='user':
            session['session_cart'].clear()  
            flash("Purchase Canceled")
            return redirect(url_for('user_page'))
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')
    
@app.route('/user/history')
def user_history():
    if session.get('current_user'):
        if session['current_user']['role']=='user':
            user = User.query.filter_by(username=session['current_user']['username']).first()
            return render_template('history.html', orders=user.orders)
        else:
            return render_template('login_user.html')
    else:
        return render_template('login_user.html')