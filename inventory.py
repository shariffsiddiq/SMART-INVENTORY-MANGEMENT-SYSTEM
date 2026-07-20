import sqlite3
from datetime import date
from getpass import getpass

DB_PATH = "inventory.db"
LOW_STOCK_THRESHOLD = 5
DEFAULT_ADMIN = {"username": "siddiq", "password": "siddiq"}


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(connection):
    with connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                supplier TEXT,
                created_at DATE DEFAULT CURRENT_DATE
            )
        """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                sale_date DATE NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """
        )
        admin = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            (DEFAULT_ADMIN["username"],),
        ).fetchone()
        if not admin:
            connection.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (DEFAULT_ADMIN["username"], DEFAULT_ADMIN["password"]),
            )

def prompt_positive_integer(label):
    while True:
        value = input(f"{label}: ").strip()
        if not value.isdigit() or int(value) < 0:
            print("Please enter a valid non-negative integer.")
            continue
        return int(value)


def prompt_nonempty_text(label):
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("This field cannot be empty.")


def login(connection):
    print("\n=== Admin Login ===")
    username = input("Username: ").strip()
    password = getpass("Password: ")
    user = connection.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    if user:
        print(f"\nWelcome, {username}!\n")
        return True
    print("Invalid credentials. Please try again.\n")
    return False


def add_product(connection):
    print("\n--- Add Product ---")
    product_name = prompt_nonempty_text("Product Name")
    category = prompt_nonempty_text("Category")
    price = None
    while price is None:
        raw_price = input("Price: ").strip()
        try:
            price = float(raw_price)
            if price < 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid non-negative number for price.")
            price = None
    quantity = prompt_positive_integer("Quantity")
    supplier = prompt_nonempty_text("Supplier")
    with connection:
        connection.execute(
            "INSERT INTO products (product_name, category, price, quantity, supplier) VALUES (?, ?, ?, ?, ?)",
            (product_name, category, price, quantity, supplier),
        )
    print(f"Product '{product_name}' added successfully.\n")


def list_products(connection):
    products = connection.execute(
        "SELECT id, product_name, category, price, quantity, supplier FROM products ORDER BY id"
    ).fetchall()
    if not products:
        print("No products found. Add a product first.\n")
        return []

    print("\nCurrent Products:")
    print("ID  Product Name                  Category      Price     Qty  Supplier")
    print("--  ---------------------------- ------------- -------- ---- ----------------")
    for product in products:
        print(
            f"{product['id']:2}  {product['product_name'][:28]:28} {product['category'][:12]:12} {product['price']:8.2f} {product['quantity']:4} {product['supplier'][:16]:16}"
        )
    print()
    return products


def select_product(connection, prompt_text="Select product ID"):
    products = list_products(connection)
    if not products:
        return None
    product_ids = {product["id"] for product in products}
    while True:
        selected = input(f"{prompt_text}: ").strip()
        if not selected.isdigit() or int(selected) not in product_ids:
            print("Enter a valid product ID from the list.")
            continue
        return int(selected)


def sell_product(connection):
    print("\n--- Sell Product ---")
    product_id = select_product(connection)
    if product_id is None:
        return

    product = connection.execute(
        "SELECT product_name, price, quantity FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()
    if not product:
        print("Product not found.\n")
        return

    print(f"Selected: {product['product_name']} (Stock: {product['quantity']})")
    quantity = prompt_positive_integer("Quantity to sell")
    if quantity == 0:
        print("Sale cancelled. Quantity must be greater than 0.\n")
        return
    if quantity > product["quantity"]:
        print("Insufficient stock. Sale cannot be completed.\n")
        return

    total_amount = round(quantity * product["price"], 2)
    with connection:
        connection.execute(
            "UPDATE products SET quantity = quantity - ? WHERE id = ?",
            (quantity, product_id),
        )
        connection.execute(
            "INSERT INTO sales (product_id, quantity, total_amount, sale_date) VALUES (?, ?, ?, ?)",
            (product_id, quantity, total_amount, date.today().isoformat()),
        )

    print(f"Sold {quantity} x {product['product_name']} for ₹{total_amount:.2f}.\n")
    check_low_stock(connection, product_id)


def purchase_stock(connection):
    print("\n--- Purchase Stock ---")
    product_id = select_product(connection)
    if product_id is None:
        return

    product = connection.execute(
        "SELECT product_name, quantity FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()
    if not product:
        print("Product not found.\n")
        return

    print(f"Selected: {product['product_name']} (Current stock: {product['quantity']})")
    quantity = prompt_positive_integer("Quantity to add")
    if quantity == 0:
        print("Purchase cancelled. Quantity must be greater than 0.\n")
        return

    with connection:
        connection.execute(
            "UPDATE products SET quantity = quantity + ? WHERE id = ?",
            (quantity, product_id),
        )
    print(f"Added {quantity} units to '{product['product_name']}'.\n")


def search_product(connection):
    print("\n--- Search Product ---")
    keyword = prompt_nonempty_text("Search keyword")
    query = "%" + keyword + "%"
    products = connection.execute(
        "SELECT id, product_name, category, price, quantity, supplier FROM products WHERE product_name LIKE ? OR category LIKE ? ORDER BY product_name",
        (query, query),
    ).fetchall()
    if not products:
        print("No products matched your search.\n")
        return

    print("\nSearch Results:")
    for product in products:
        print(f"ID: {product['id']}")
        print(f"Product: {product['product_name']}")
        print(f"Category: {product['category']}")
        print(f"Price: ₹{product['price']:.2f}")
        print(f"Stock: {product['quantity']}")
        print(f"Supplier: {product['supplier']}")
        print("-" * 40)
    print()


def today_sales_report(connection):
    print("\n--- Today's Sales ---")
    today = date.today().isoformat()
    result = connection.execute(
        "SELECT SUM(total_amount) AS total_sales FROM sales WHERE sale_date = ?",
        (today,),
    ).fetchone()
    total_sales = result["total_sales"] or 0.0
    print(f"Today's Sales: ₹{total_sales:.2f}\n")


def top_selling_products(connection):
    print("\n--- Top Selling Products ---")
    rows = connection.execute(
        """
        SELECT p.product_name, SUM(s.quantity) AS total_sold
        FROM sales s
        JOIN products p ON p.id = s.product_id
        GROUP BY p.product_name
        ORDER BY total_sold DESC
        LIMIT 5
        """,
    ).fetchall()
    if not rows:
        print("No sales records available yet.\n")
        return

    print("Product Name                        Total Sold")
    print("----------------------------------- ----------")
    for row in rows:
        print(f"{row['product_name'][:35]:35} {row['total_sold']:10}")
    print()


def dashboard(connection):
    print("\n=== Sales Dashboard ===")
    total_products = connection.execute("SELECT COUNT(*) AS count FROM products").fetchone()["count"]
    total_stock = connection.execute("SELECT SUM(quantity) AS total_qty FROM products").fetchone()["total_qty"] or 0
    low_stock_items = connection.execute(
        "SELECT product_name, quantity FROM products WHERE quantity < ? ORDER BY quantity",
        (LOW_STOCK_THRESHOLD,),
    ).fetchall()
    today = date.today().isoformat()
    today_sales = connection.execute(
        "SELECT SUM(total_amount) AS total_sales FROM sales WHERE sale_date = ?",
        (today,),
    ).fetchone()["total_sales"] or 0.0

    print(f"Total Products: {total_products}")
    print(f"Available Stock: {total_stock}")
    print(f"Today's Sales: ₹{today_sales:.2f}")
    print("\nLow Stock Items:")
    if low_stock_items:
        for item in low_stock_items:
            print(f"- {item['product_name']} (Remaining: {item['quantity']})")
    else:
        print("None")

    print("\nTop 5 Selling Products:")
    rows = connection.execute(
        """
        SELECT p.product_name, SUM(s.quantity) AS total_sold
        FROM sales s
        JOIN products p ON p.id = s.product_id
        GROUP BY p.product_name
        ORDER BY total_sold DESC
        LIMIT 5
        """,
    ).fetchall()
    if rows:
        for row in rows:
            print(f"- {row['product_name']} (Sold: {row['total_sold']})")
    else:
        print("No sales data yet.")
    print()


def check_low_stock(connection, product_id):
    product = connection.execute(
        "SELECT product_name, quantity FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()
    if product and product["quantity"] < LOW_STOCK_THRESHOLD:
        print("⚠ Low Stock Alert")
        print(f"{product['product_name']}")
        print(f"Remaining: {product['quantity']}\n")


def main():
    connection = get_connection()
    init_db(connection)

    while not login(connection):
        pass

    while True:
        print("1. Add Product")
        print("2. Sell Product")
        print("3. Purchase Stock")
        print("4. Search Product")
        print("5. Today's Sales")
        print("6. Top Selling Products8")
        print("7. Dashboard")
        print("8. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_product(connection)
        elif choice == "2":
            sell_product(connection)
        elif choice == "3":
            purchase_stock(connection)
        elif choice == "4":
            search_product(connection)
        elif choice == "5":
            today_sales_report(connection)
        elif choice == "6":
            top_selling_products(connection)
        elif choice == "7":
            dashboard(connection)
        elif choice == "8":
            print("Exiting the Inventory Management System. Goodbye!\n")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 8.\n")

    connection.close()


if __name__ == "__main__":
    main()
