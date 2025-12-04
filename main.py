from flask import Flask
from database import get_products,get_sales

app = Flask(__name__)

@app.route('/')
def home():
    return "This is the index route"

@app.route('/products')
def fetch_products():
    products = get_products()
    return products

@app.route('/sales')
def fetch_sales():
    sales = get_sales()
    return sales

@app.route('/dashboard')
def dashboard():
    return "This is the dashboard route"

@app.route('/register')
def register():
    return "This is the register route"

@app.route('/log-in')
def log_in():
    return "This is the log-in route"

    
app.run()