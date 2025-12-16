import psycopg2

conn = psycopg2.connect(host="localhost", port="5432", user="postgres", password="Colesprouse2311!", dbname="myduka_db")

cur = conn.cursor()

def get_products():
    cur.execute("select * from products")
    products = cur.fetchall()
    return products

products = get_products()    

def insert_products(values):
    cur.execute(f"insert into products(name,buying_price,selling_price) values{values}")
    conn.commit()

# my_product = ('Samsung', 100000, 120000)

# my_product2 = ('Iphone', 200000, 250000)
# insert_products(my_product)
# insert_products(my_product2)
print(products)

def insert_sales(values):
    cur.execute(f"insert into sales(pid, quantity)values{values}")
    conn.commit()

# my_sale = (1, 700)
# my_sale2 = (2, 49)
# insert_sales(my_sale)
# insert_sales(my_sale2)

def insert_sales_2(values):
    cur.execute("insert into sales(pid,quantity)values(%s,%s)",(values))
    conn.commit()

# sale_1 = (49,200)
# insert_sales_2(sale_1)

def get_sales():
    cur.execute("select * from sales")
    sales = cur.fetchall()
    return sales

sales = get_sales()
print(sales)

def insert_users(values):
    cur.execute('insert into users(full_name,email,phone_number,password)values(%s,%s,%s,%s)', (values))
    conn.commit()

def get_users():
    cur.execute('select * from users')
    users = cur.fetchall()
    return users

# user_1 =('John Doe', 'johnd@mail.com', '0111239415', 'mypass')
# insert_users(user_1)
#get the users 
users = get_users()
print(users)

# availabe stock
def available_stock(product_id):
    cur.execute(f'select sum(stock_quantity) from stock where pid={product_id}')
    total_stock = cur.fetchone()[0] or 0

    cur.execute(f"select sum(quantity) from sales where pid = {product_id}")
    total_sales = cur.fetchone()[0] or 0

    current_stock = total_stock - total_sales
    return current_stock

stock = available_stock(1)
print(stock)

# insert stock
def insert_stock(values):
    cur.execute(
        f"insert into stock (pid,stock_quantity)values{values}",  
    )
    conn.commit()
    
# stock
def get_stock():     
    cur.execute("select * from stock")
    stock = cur.fetchall()
    return stock

def check_user_exists(email):
    cur.execute("select * from users where email = %s", (email,))
    user = cur.fetchone()
    return user

#sales per product

