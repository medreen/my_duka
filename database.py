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

my_product = ('Samsung', 100000, 120000)
my_product2 = ('Iphone', 200000, 250000)
insert_products(my_product)
insert_products(my_product2)
print(products)

def insert_sales(values):
    cur.execute(f"insert into sales(pid, quantity)values{values}")
    conn.commit()

my_sale = (1, 700)
my_sale2 = (2, 49)
insert_sales(my_sale)
insert_sales(my_sale2)


def get_sales():
    cur.execute("select * from sales")
    sales = cur.fetchall()
    return sales

sales = get_sales()
print(sales)


