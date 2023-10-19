from flask import render_template, request, session,redirect,url_for
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

@app.route('/')
def index():
    search_query = request.args.get('search_query')
    products=None
    if search_query:
        products = search(search_query)
    else:
        products = Product.query.all() 
    categories = Category.query.all()
    mode="all"
    return render_template('content_page.html', products=products, categories=categories, mode=mode)
    
@app.route('/category/<int:category_id>')
def index_page_by_category(category_id):
    search_query = request.args.get('search_query')
    products=None
    if search_query:
        products = search(search_query)
    else:
        products = Product.query.filter_by(category_id=category_id).all()
    category = Category.query.filter_by(id=category_id).first()
    mode="one"
    return render_template('content_page.html', products=products, category=category, mode=mode)
    
