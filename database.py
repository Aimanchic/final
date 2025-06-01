import sqlite3

def get_connection():
    return sqlite3.connect("bakery.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            price REAL DEFAULT 0
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('owner', 'employee'))
        );
    """)
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?);",
                       ('admin', 'admin123', 'owner'))
    conn.commit()
    conn.close()

def create_extended_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            quantity INTEGER DEFAULT 0,
            price REAL DEFAULT 0
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS item_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (item_id) REFERENCES items(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)
    conn.commit()
    conn.close()


def add_product(name, category, quantity, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, category, quantity, price) VALUES (?, ?, ?, ?);",
                   (name, category, quantity, price))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products;")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_products_dict():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM products;")
    result = cursor.fetchall()
    conn.close()
    return {id_: name for id_, name in result}

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def register_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?);",
                       (username, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    result = cursor.fetchall()
    conn.close()
    return result

def delete_user(username):
    if username == "admin":
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def add_item(name, ingredients, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, price))
    item_id = cursor.lastrowid
    for product_id, qty in ingredients:
        cursor.execute("INSERT INTO item_ingredients (item_id, product_id, quantity) VALUES (?, ?, ?);",
                       (item_id, product_id, qty))
    conn.commit()
    conn.close()

def get_all_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM items WHERE name != ''")
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items

def update_product(product_id, name, category, quantity, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET name = ?, category = ?, quantity = ?, price = ?
        WHERE id = ?
    """, (name, category, quantity, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def get_all_items_full():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, quantity, price
        FROM items
        WHERE name != ''
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def increase_item_quantity(item_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM items WHERE name = ?", (item_name,))
    item_row = cursor.fetchone()
    if not item_row:
        conn.close()
        return False
    item_id = item_row[0]

    cursor.execute("""
        SELECT product_id, quantity
        FROM item_ingredients
        WHERE item_id = ?
    """, (item_id,))
    ingredients = cursor.fetchall()

    for product_id, required_qty in ingredients:
        cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if not row or row[0] < required_qty:
            conn.close()
            return False

    for product_id, required_qty in ingredients:
        cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (required_qty, product_id))

    cursor.execute("UPDATE items SET quantity = quantity + 1 WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()
    return True

def decrease_item_quantity(item_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM items WHERE name = ?", (item_name,))
    item_row = cursor.fetchone()
    if not item_row:
        conn.close()
        return False
    item_id = item_row[0]

    cursor.execute("SELECT quantity FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    if not row or row[0] < 1:
        conn.close()
        return False

    cursor.execute("UPDATE items SET quantity = quantity - 1 WHERE id = ?", (item_id,))

    cursor.execute("SELECT product_id, quantity FROM item_ingredients WHERE item_id = ?", (item_id,))
    ingredients = cursor.fetchall()
    for product_id, qty in ingredients:
        cursor.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?", (qty, product_id))

    conn.commit()
    conn.close()
    return True

#def debug_show_users():
#    conn = get_connection()
#    cursor = conn.cursor()
#    cursor.execute("SELECT username, password, role FROM users")
#    for row in cursor.fetchall():
#        print(f"{row}")
#    conn.close()
