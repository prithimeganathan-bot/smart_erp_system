# Smart ERP System

A full-stack Enterprise Resource Planning web application built with Python Flask and MySQL.

## Features
- Role-based authentication (Admin/Staff)
- Product inventory management
- Multi-item sales invoicing
- Purchase management with auto stock update
- Analytics dashboard with Chart.js
- Dark/Light theme toggle

## Tech Stack
- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** Chart.js
- **Icons:** Font Awesome

## Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `config.py` with your database credentials:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'smart_erp'
```
6. Run the app: `python app.py`
7. Open browser: `http://127.0.0.1:5000`