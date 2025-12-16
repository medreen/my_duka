from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_products,get_sales,insert_products,insert_sales,available_stock,get_stock,insert_stock,check_user_exists, insert_users

# assigning an object to flask/ instance of flask
app = Flask(__name__)

#session secret_key
app.secret_key = '893479jkkk42904829qawij8742'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/products')
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

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        password = request.form['password']

        existing_user = check_user_exists(email)
        if not existing_user:
            new_user = (full_name,email,phone_number,password)
            insert_users(new_user)
            flash('User registered succsessfully', 'success')
            return redirect(url_for('log_in'))
        else:
            flash('Account is already registered.')
    return render_template('register.html')


@app.route('/login')
def log_in():
    return render_template("login.html")

# @app.route('/test/<int:user_id>')
# def test(user_id):
#     return {"id":user_id}

    
app.run(debug=True)