import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection
def get_db_conn():
    return psycopg2.connect(
        host="localhost", 
        port="5432", 
        user="postgres", 
        password="Colesprouse2311!", 
        dbname="myduka_db"
    )

def get_products():
    with get_db_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM products")
            return cur.fetchall()

def get_sales():
    with get_db_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT s.id, p.name, s.quantity, s.created_at
                FROM sales s 
                JOIN products p ON s.pid = p.id
                ORDER BY s.created_at DESC
            """)
            return cur.fetchall()

def insert_users(values):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO users(full_name,email,phone_number,password) VALUES (%s,%s,%s,%s)', values)
            conn.commit()

def check_user_exists(email):
    with get_db_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cur.fetchone()

def available_stock(product_id):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT SUM(stock_quantity) FROM stock WHERE pid=%s', (product_id,))
            total_stock = cur.fetchone()[0] or 0
            cur.execute("SELECT SUM(quantity) FROM sales WHERE pid = %s", (product_id,))
            total_sales = cur.fetchone()[0] or 0
            return total_stock - total_sales

def get_dashboard_stats():
    with get_db_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # ::FLOAT ensures Python can convert the Decimal types for JSON
            cur.execute("""
                SELECT 
                    COALESCE(SUM(s.quantity * p.selling_price), 0)::FLOAT as revenue,
                    COALESCE(SUM(s.quantity * (p.selling_price - p.buying_price)), 0)::FLOAT as profit
                FROM sales s
                JOIN products p ON s.pid = p.id;
            """)
            return cur.fetchone()

def get_chart_data():
    with get_db_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT p.name, SUM(s.quantity)::FLOAT as qty
                FROM sales s
                JOIN products p ON s.pid = p.id
                GROUP BY p.name
            """)
            return cur.fetchall()
        
def insert_products(values):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO products(name, buying_price, selling_price) VALUES (%s, %s, %s)', values)
            conn.commit()

def insert_sales(pid, quantity):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO sales(pid, quantity) VALUES (%s, %s)', (pid, quantity))
            conn.commit()

def insert_stock(pid, quantity):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO stock(pid, stock_quantity) VALUES (%s, %s)', (pid, quantity))
            conn.commit()

def get_stock():
    with get_db_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT st.id, p.name, st.stock_quantity, st.created_at
                FROM stock st
                JOIN products p ON st.pid = p.id
                ORDER BY st.created_at DESC
            """)
            return cur.fetchall()
        