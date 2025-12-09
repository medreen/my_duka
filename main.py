from flask import Flask, render_template, request, redirect, url_for
from database import get_products,get_sales, insert_products

# assigning an object to flask/ instance of flask
app = Flask(__name__)

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
    return redirect(url_for('fetch_products'))

@app.route('/sales')
def fetch_sales():
    sales = get_sales()
    return render_template('sales.html', sales = sales)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/log-in')
def log_in():
    return render_template("login.html")

# @app.route('/test/<int:user_id>')
# def test(user_id):
#     return {"id":user_id}

    
app.run(debug=True)