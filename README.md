# 🏢 Smart ERP System

A full-stack **Enterprise Resource Planning (ERP)** web application built with Python Flask and MySQL. Designed for small to medium businesses to manage inventory, sales, purchases, and staff accounts — all in one place.

---

## 📸 Features

- 🔐 **Role-Based Authentication** — Separate Admin and Staff access levels
- 📦 **Product Management** — Full CRUD with category support and low stock alerts
- 🧾 **Sales Invoicing** — Multi-item invoices with automatic stock deduction
- 🚚 **Purchase Management** — Record supplier purchases with auto stock increase
- 📊 **Analytics Dashboard** — 4 interactive charts (monthly sales, sales vs purchase, category pie, top products)
- 👥 **User Management** — Admin can create, assign roles, and delete staff accounts
- 🌙 **Dark / Light Theme** — Toggle with preference saved across sessions
- 🔍 **Live Search** — Search products, sales history, and purchases instantly

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Database | MySQL |
| Frontend | HTML5, CSS3, JavaScript (ES6) |
| Charts | Chart.js |
| Icons | Font Awesome 6 |
| Security | Werkzeug (password hashing) |

---

## 📁 Project Structure

```
smart_inventory_system/
│
├── app.py                  # Main Flask application (all routes)
├── config.py               # Database configuration (not in repo)
├── requirements.txt        # Python dependencies
│
├── templates/
│   ├── base.html           # Shared sidebar layout
│   ├── login.html          # Login page
│   ├── dashboard.html      # Analytics dashboard
│   ├── products.html       # Product management
│   ├── purchase.html       # Purchase management
│   ├── sales.html          # Sales invoicing
│   └── users.html          # User management (Admin only)
│
└── static/
    ├── css/
    │   └── style.css       # Global stylesheet with theme support
    └── logo.png            # Application logo
```

---

## 🗄️ Database Schema

```
users           → Login accounts with roles (admin/staff)
categories      → Product categories
products        → Inventory with stock levels and reorder alerts
suppliers       → Vendor information
purchase_bills  → Purchase invoice headers
purchase_items  → Line items for each purchase
sales_invoices  → Sales invoice headers
sales_items     → Line items for each sale with profit tracking
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/prithimeganathan-bot/smart_erp_system.git
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Activate it:**

Windows:
```bash
venv\Scripts\activate.bat
```

Mac/Linux:
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE smart_erp;
USE smart_erp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin','staff') DEFAULT 'staff'
);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INT,
    cost_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    reorder_level INT DEFAULT 5,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL,
    contact VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE purchase_bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    total_amount DECIMAL(10,2) DEFAULT 0,
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE purchase_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    product_id INT,
    quantity INT,
    purchase_price DECIMAL(10,2),
    FOREIGN KEY (bill_id) REFERENCES purchase_bills(bill_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE sales_invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(150) DEFAULT 'Walk-in Customer',
    total_amount DECIMAL(10,2) DEFAULT 0,
    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT,
    product_id INT,
    quantity INT,
    selling_price DECIMAL(10,2),
    profit DECIMAL(10,2),
    FOREIGN KEY (invoice_id) REFERENCES sales_invoices(invoice_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO categories (category_name) VALUES
('Electronics'), ('Clothing'), ('Food & Beverages'), ('Furniture');

INSERT INTO suppliers (supplier_name, contact, email) VALUES
('ABC Traders', '9876543210', 'abc@traders.com');
```

### 5. Create Admin User

Create a file called `create_admin.py` and run it once:

```python
from werkzeug.security import generate_password_hash
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='smart_erp'
)
cursor = conn.cursor()
hashed = generate_password_hash('admin123')
cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
    ('admin', hashed, 'admin')
)
conn.commit()
cursor.close()
conn.close()
print("Admin created successfully!")
```

```bash
python create_admin.py
```

### 6. Create config.py

Create a file called `config.py` in the project root:

```python
MYSQL_HOST     = 'localhost'
MYSQL_USER     = 'root'
MYSQL_PASSWORD = 'your_password_here'
MYSQL_DB       = 'smart_erp'
```

### 7. Run the Application

```bash
python app.py
```

Open your browser and go to:
```
http://127.0.0.1:5000
```

**Default Login:**
```
Username: admin
Password: admin123
```

---

## 🔐 User Roles

| Feature | Admin | Staff |
|---------|-------|-------|
| View Dashboard | ✅ | ✅ |
| View Products | ✅ | ✅ |
| Add / Edit / Delete Products | ✅ | ❌ |
| Record Sales | ✅ | ✅ |
| Record Purchases | ✅ | ✅ |
| Manage Users | ✅ | ❌ |
| View Analytics | ✅ | ✅ |

---

## 📊 Dashboard Charts

| Chart | Description |
|-------|-------------|
| Monthly Sales | Bar chart showing revenue per month for current year |
| Sales vs Purchase | Grouped bar chart comparing money in vs money out |
| Sales by Category | Doughnut chart showing category-wise revenue percentage |
| Top Products | Ranked list of best selling products per category |

---

## 🔒 Security Features

- Passwords hashed using **PBKDF2-SHA256** via Werkzeug
- Sessions encrypted with Flask secret key
- Role-based route protection using custom decorators
- Staff users blocked from admin routes at the server level
- Database transactions prevent partial/corrupt data on sales

---

## 📦 Dependencies

```
Flask
mysql-connector-python
Werkzeug
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🚀 Future Enhancements

- [ ] PDF invoice generation
- [ ] Export sales/products to Excel
- [ ] Profit & Loss report page
- [ ] Email alerts for low stock
- [ ] Barcode scanner integration
- [ ] Multi-branch support

---

## 👨‍💻 Author

Built as a portfolio project demonstrating full-stack web development with Python Flask, MySQL, and modern frontend technologies.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
