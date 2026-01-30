from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_products,get_sales,insert_products,insert_sales,available_stock,get_stock,insert_stock,check_user_exists, insert_users
from flask_bcrypt import Bcrypt
from functools import wraps
import json
from database import * # Ensure all functions above are imported

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
    return render_template("products.html", products = products)

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
    return render_template('sales.html', sales = sales, products = products)

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
    return render_template('stock.html', stock = stock, products = products)


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