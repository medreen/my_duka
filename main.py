from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_products,get_sales,insert_products,insert_sales,available_stock,get_stock,insert_stock,check_user_exists, insert_users
from flask_bcrypt import Bcrypt
from functools import wraps
import json
from database import * # Ensure all functions above are imported
from datetime import datetime, timedelta
from collections import Counter

# assigning an object to flask/ instance of flask
app = Flask(__name__)

#creating decrypt object
bcrypt = Bcrypt(app)

#session secret_key
app.secret_key = '893479jkkk42904829qawij8742'

@app.route('/')
def home():
    return render_template("index.html")

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('log_in'))
        return f(*args,**kwargs)
    return protected

@app.route('/products')
@login_required
def fetch_products():
    products = get_products()
    
    # Calculate stats
    low_stock_count = sum(1 for p in products if available_stock(p['id']) < 5)
    in_stock_count = sum(1 for p in products if available_stock(p['id']) > 0)
    
    # Calculate total inventory value
    total_value = sum(available_stock(p['id']) * float(p['buying_price']) for p in products)
    
    return render_template("products.html", 
                          products=products,
                          low_stock_count=low_stock_count,
                          in_stock_count=in_stock_count,
                          total_inventory_value=total_value,
                          available_stock=available_stock)


@app.route('/add_products', methods = ['GET', 'POST'])
def add_products():
    product_name = request.form['product_name']
    buying_price = request.form["buying_price"]
    selling_price = request.form["selling_price"]
    new_product = (product_name, buying_price, selling_price)
    insert_products(new_product)
    flash('Product added successfully', 'success')
    return redirect(url_for('fetch_products'))

@app.route('/sales')
@login_required
def fetch_sales():    
    sales = get_sales()
    products = get_products()
    
    # Calculate stats
    today = datetime.now().date()
    today_sales_count = sum(1 for s in sales if s['created_at'].date() == today)
    total_units_sold = sum(s['quantity'] for s in sales)
    
    # Top product
    product_counter = Counter(s['name'] for s in sales)
    top_product_name = product_counter.most_common(1)[0][0] if product_counter else "N/A"
    
    # Chart data (last 7 days)
    last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    sales_by_date = {date: 0 for date in last_7_days}
    for s in sales:
        date_str = s['created_at'].strftime('%Y-%m-%d')
        if date_str in sales_by_date:
            sales_by_date[date_str] += s['quantity']
    
    sales_chart_labels = list(sales_by_date.keys())
    sales_chart_data = list(sales_by_date.values())
    
    return render_template('sales.html', 
                          sales=sales, 
                          products=products,
                          today_sales_count=today_sales_count,
                          total_units_sold=total_units_sold,
                          top_product_name=top_product_name,
                          sales_chart_labels=json.dumps(sales_chart_labels),
                          sales_chart_data=json.dumps(sales_chart_data))


@app.route('/add_sales', methods = ['GET', 'POST'])
def add_sales():
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    new_sale = (product_id, quantity)
    check_stock = available_stock(product_id)
    if check_stock < float(quantity):
        flash('Insuficient stock', 'danger')
        return redirect(url_for('fetch_sales'))
    insert_sales(new_sale)
    flash('Sale made succesfully', 'success')
    return redirect(url_for('fetch_sales'))


@app.route('/stock')
@login_required
def fetch_stock():
    stock = get_stock()
    products = get_products()
    
    # Calculate stats
    total_stock_added = sum(s['stock_quantity'] for s in stock)
    latest_stock_product = stock[0]['name'] if stock else "N/A"
    
    # Stock value (approximate)
    stock_value = sum(s['stock_quantity'] * 100 for s in stock)  # Simplified calculation
    
    # Chart data (last 7 days)
    today = datetime.now().date()
    last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    stock_by_date = {date: 0 for date in last_7_days}
    for s in stock:
        date_str = s['created_at'].strftime('%Y-%m-%d')
        if date_str in stock_by_date:
            stock_by_date[date_str] += s['stock_quantity']
    
    stock_chart_labels = list(stock_by_date.keys())
    stock_chart_data = list(stock_by_date.values())
    
    return render_template('stock.html', 
                          stock=stock, 
                          products=products,
                          total_stock_added=total_stock_added,
                          latest_stock_product=latest_stock_product,
                          stock_value=stock_value,
                          stock_chart_labels=json.dumps(stock_chart_labels),
                          stock_chart_data=json.dumps(stock_chart_data))

@app.route('/add_stock', methods = ['GET', 'POST'])
def add_stock():
    product_id = request.form['product_id']
    stock_quantity = request.form["stock_quantity"]    
    new_stock = (product_id, stock_quantity)
    insert_stock(new_stock)
    return redirect(url_for('fetch_stock'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        password = request.form['password']

        existing_user = check_user_exists(email)
        if not existing_user:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = (full_name,email,phone_number,hashed_password)
            insert_users(new_user)
            flash('User registered succsessfully', 'success')
            return redirect(url_for('log_in'))
        else:
            flash('Account is already registered.')
    return render_template('register.html')


@app.route('/login', methods=["POST", 'GET'])
def log_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        registered_user = check_user_exists(email)

        if not registered_user:            
            flash('User does not exist.', 'danger')
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(registered_user[-1],password):
                session['email'] = email
                flash('Login successful', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash("Check login information.", 'danger')
    return render_template("login.html")

@app.route('/dashboard')
@login_required
def dashboard():
    # Use the optimized database functions
    stats = get_dashboard_stats()
    chart_data = get_chart_data()
    products = get_products()
    
    # Extract stats
    total_revenue = stats['revenue']
    total_profit = stats['profit']
    
    # Prepare chart data
    labels = [row['name'] for row in chart_data]
    values = [row['qty'] for row in chart_data]
    
    # Low stock logic
    low_stock = []
    for p in products:
        count = available_stock(p['id'])
        if count < 5:
            low_stock.append({'name': p['name'], 'count': count})

    return render_template("dashboard.html", 
                           revenue=total_revenue, 
                           profit=total_profit,
                           labels=json.dumps(labels),
                           sales_values=json.dumps(values),
                           num_products=len(products),
                           low_stock_count=len(low_stock))
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully. Catch you on the flip side!', 'info')
    return redirect(url_for('home'))


    
app.run(debug=True)