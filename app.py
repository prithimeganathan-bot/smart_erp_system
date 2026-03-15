from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "smarterp_secret_2026"

# ---------------- DB CONNECTION ----------------

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='smart_erp'
    )

# ---------------- DECORATORS ----------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated

# ---------------- AUTH ----------------

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password, role FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            return redirect(url_for('dashboard'))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT product_name, stock_quantity FROM products WHERE stock_quantity <= reorder_level")
    low_stock_products = cursor.fetchall()

    cursor.execute("SELECT IFNULL(SUM(total_amount),0) FROM sales_invoices WHERE DATE(invoice_date)=CURDATE()")
    today_sales = cursor.fetchone()[0]

    cursor.execute("""
        SELECT IFNULL(SUM(total_amount),0) FROM sales_invoices
        WHERE MONTH(invoice_date)=MONTH(CURDATE()) AND YEAR(invoice_date)=YEAR(CURDATE())
    """)
    monthly_sales = cursor.fetchone()[0]

    cursor.execute("SELECT IFNULL(SUM(total_amount),0) FROM sales_invoices")
    overall_sales = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return render_template("dashboard.html",
                           total_products=total_products,
                           low_stock_products=low_stock_products,
                           today_sales=today_sales,
                           monthly_sales=monthly_sales,
                           overall_sales=overall_sales)

# ---------------- PRODUCTS ----------------

@app.route('/products_page')
@login_required
def products_page():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT category_id, category_name FROM categories ORDER BY category_name")
    categories = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("products.html", categories=categories)

@app.route('/products')
@login_required
def get_products():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.product_id, p.product_name, c.category_name,
               p.cost_price, p.selling_price, p.stock_quantity, p.reorder_level
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.product_id DESC
    """)
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(products)

@app.route('/add_product', methods=['POST'])
@login_required
@admin_required
def add_product():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO products (product_name, category_id, cost_price, selling_price, stock_quantity, reorder_level)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['product_name'], data['category_id'], data['cost_price'],
          data['selling_price'], data['stock_quantity'], data.get('reorder_level', 5)))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Product added successfully"})

@app.route('/update_product/<int:product_id>', methods=['PUT'])
@login_required
@admin_required
def update_product(product_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE products SET product_name=%s, category_id=%s, cost_price=%s,
        selling_price=%s, stock_quantity=%s, reorder_level=%s
        WHERE product_id=%s
    """, (data['product_name'], data['category_id'], data['cost_price'],
          data['selling_price'], data['stock_quantity'], data.get('reorder_level', 5), product_id))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Product updated successfully"})

@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Product deleted successfully"})

# ---------------- CATEGORIES ----------------

@app.route('/categories')
@login_required
def get_categories():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories ORDER BY category_name")
    categories = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(categories)

# ---------------- SUPPLIERS ----------------

@app.route('/suppliers')
@login_required
def get_suppliers():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers ORDER BY supplier_name")
    suppliers = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(suppliers)

@app.route('/add_supplier', methods=['POST'])
@login_required
@admin_required
def add_supplier():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO suppliers (supplier_name, contact, email)
        VALUES (%s, %s, %s)
    """, (data['supplier_name'], data.get('contact', ''), data.get('email', '')))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Supplier added successfully"})

# ---------------- PURCHASE ----------------

@app.route('/purchase_page')
@login_required
def purchase_page():
    return render_template("purchase.html")

@app.route('/create_purchase', methods=['POST'])
@login_required
def create_purchase():
    data = request.get_json()
    supplier_id = data['supplier_id']
    items = data['items']

    db = get_db()
    cursor = db.cursor()
    total_amount = 0

    cursor.execute("INSERT INTO purchase_bills (supplier_id, total_amount) VALUES (%s, 0)", (supplier_id,))
    bill_id = cursor.lastrowid

    for item in items:
        product_id = item['product_id']
        quantity = int(item['quantity'])
        price = float(item['price'])
        total_amount += quantity * price

        cursor.execute("""
            INSERT INTO purchase_items (bill_id, product_id, quantity, purchase_price)
            VALUES (%s, %s, %s, %s)
        """, (bill_id, product_id, quantity, price))

        cursor.execute("""
            UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id=%s
        """, (quantity, product_id))

    cursor.execute("UPDATE purchase_bills SET total_amount=%s WHERE bill_id=%s", (total_amount, bill_id))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Purchase recorded successfully", "bill_id": bill_id})

@app.route('/get_purchases')
@login_required
def get_purchases():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT pb.bill_id, s.supplier_name, pb.total_amount, pb.bill_date
        FROM purchase_bills pb
        JOIN suppliers s ON pb.supplier_id = s.supplier_id
        ORDER BY pb.bill_date DESC
        LIMIT 50
    """)
    purchases = cursor.fetchall()
    for p in purchases:
        p['bill_date'] = str(p['bill_date'])
    cursor.close()
    db.close()
    return jsonify(purchases)

# ---------------- SALES ----------------

@app.route('/sales_page')
@login_required
def sales_page():
    return render_template("sales.html")

@app.route('/create_sale', methods=['POST'])
@login_required
def create_sale():
    data = request.get_json()
    customer_name = data.get('customer_name', 'Walk-in Customer')
    items = data['items']

    db = get_db()
    cursor = db.cursor()
    total_amount = 0

    cursor.execute("INSERT INTO sales_invoices (customer_name, total_amount) VALUES (%s, 0)", (customer_name,))
    invoice_id = cursor.lastrowid

    try:
        for item in items:
            product_id = item['product_id']
            quantity = int(item['quantity'])

            cursor.execute("SELECT selling_price, cost_price, stock_quantity FROM products WHERE product_id=%s", (product_id,))
            row = cursor.fetchone()
            selling_price, cost_price, stock = row

            if quantity > stock:
                db.rollback()
                return jsonify({"message": f"Not enough stock. Available: {stock}"}), 400

            profit = (selling_price - cost_price) * quantity
            total_amount += selling_price * quantity

            cursor.execute("""
                INSERT INTO sales_items (invoice_id, product_id, quantity, selling_price, profit)
                VALUES (%s, %s, %s, %s, %s)
            """, (invoice_id, product_id, quantity, selling_price, profit))

            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id=%s", (quantity, product_id))

        cursor.execute("UPDATE sales_invoices SET total_amount=%s WHERE invoice_id=%s", (total_amount, invoice_id))
        db.commit()

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "Sale recorded successfully", "invoice_id": invoice_id, "total": float(total_amount)})

@app.route('/get_sales')
@login_required
def get_sales():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT si.invoice_id, si.customer_name, si.total_amount, si.invoice_date
        FROM sales_invoices si
        ORDER BY si.invoice_date DESC
        LIMIT 50
    """)
    sales = cursor.fetchall()
    for s in sales:
        s['invoice_date'] = str(s['invoice_date'])
    cursor.close()
    db.close()
    return jsonify(sales)

# ---------------- ANALYTICS ----------------

@app.route('/monthly_sales_data')
@login_required
def monthly_sales_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT MONTH(invoice_date), IFNULL(SUM(total_amount),0)
        FROM sales_invoices
        WHERE YEAR(invoice_date)=YEAR(CURDATE())
        GROUP BY MONTH(invoice_date)
        ORDER BY MONTH(invoice_date)
    """)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(data)

@app.route('/top_products')
@login_required
def top_products():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.category_name, p.product_name, SUM(si.quantity) as total_sold
        FROM sales_items si
        JOIN products p ON si.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        GROUP BY c.category_name, p.product_name
        ORDER BY c.category_name, total_sold DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(data)

# ---------------- USER MANAGEMENT (Admin only) ----------------

@app.route('/users_page')
@login_required
def users_page():
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard'))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, role FROM users ORDER BY id")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("users.html", users=users)

@app.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    data = request.get_json()
    hashed = generate_password_hash(data['password'])
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
                       (data['username'], hashed, data.get('role', 'staff')))
        db.commit()
        return jsonify({"message": "User created successfully"})
    except mysql.connector.IntegrityError:
        return jsonify({"message": "Username already exists"}), 400
    finally:
        cursor.close()
        db.close()

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    if user_id == session['user_id']:
        return jsonify({"message": "Cannot delete yourself"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "User deleted successfully"})

@app.route('/get_users')
@login_required
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, role FROM users ORDER BY id")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(users)

@app.route('/get_session_role')
def get_session_role():
    return jsonify({
        "role": session.get('role', 'staff'),
        "user_id": session.get('user_id')
    })

@app.route('/sales_vs_purchase')
@login_required
def sales_vs_purchase():
    db = get_db()
    cursor = db.cursor()

    # Monthly sales for current year
    cursor.execute("""
        SELECT MONTH(invoice_date), IFNULL(SUM(total_amount),0)
        FROM sales_invoices
        WHERE YEAR(invoice_date)=YEAR(CURDATE())
        GROUP BY MONTH(invoice_date)
    """)
    sales_data = {row[0]: float(row[1]) for row in cursor.fetchall()}

    # Monthly purchases for current year
    cursor.execute("""
        SELECT MONTH(bill_date), IFNULL(SUM(total_amount),0)
        FROM purchase_bills
        WHERE YEAR(bill_date)=YEAR(CURDATE())
        GROUP BY MONTH(bill_date)
    """)
    purchase_data = {row[0]: float(row[1]) for row in cursor.fetchall()}

    result = []
    for m in range(1, 13):
        result.append({
            "month": m,
            "sales": sales_data.get(m, 0),
            "purchase": purchase_data.get(m, 0)
        })

    cursor.close()
    db.close()
    return jsonify(result)


@app.route('/category_sales')
@login_required
def category_sales():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.category_name, IFNULL(SUM(si.quantity * si.selling_price), 0) as total
        FROM sales_items si
        JOIN products p ON si.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY total DESC
    """)
    data = [{"category": row[0], "total": float(row[1])} for row in cursor.fetchall()]
    cursor.close()
    db.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)