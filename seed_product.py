from werkzeug.security import generate_password_hash
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='smart_erp'
)
cursor = conn.cursor()

# ── INSERT CATEGORIES ──
categories = [
    'Electronics', 'Mobile Phones', 'Laptops & Computers',
    'Clothing', 'Footwear', 'Food & Beverages',
    'Home & Kitchen', 'Furniture', 'Books',
    'Sports & Fitness', 'Beauty & Personal Care', 'Toys & Games'
]

cat_ids = {}
for cat in categories:
    cursor.execute("""
        INSERT IGNORE INTO categories (category_name) VALUES (%s)
    """, (cat,))
    cursor.execute("SELECT category_id FROM categories WHERE category_name=%s", (cat,))
    cat_ids[cat] = cursor.fetchone()[0]

conn.commit()

# ── PRODUCTS DATA ──
products = [
    # Electronics
    ('Samsung 55" 4K Smart TV',       'Electronics',          28000, 34999,  50, 5),
    ('LG 43" Full HD LED TV',          'Electronics',          18000, 22999,  40, 5),
    ('Sony Bravia 65" OLED TV',        'Electronics',          75000, 89999,  20, 3),
    ('Boat Bluetooth Speaker',         'Electronics',           1500,  2499,  100,10),
    ('JBL Flip 6 Speaker',             'Electronics',           7000,  9999,  60, 5),
    ('Sony WH-1000XM5 Headphones',     'Electronics',          22000, 27999,  30, 3),
    ('boAt Airdopes 141',              'Electronics',           1200,  1999,  150,10),
    ('Canon EOS 1500D DSLR Camera',    'Electronics',          28000, 34999,  25, 3),
    ('GoPro Hero 11',                  'Electronics',          30000, 36999,  20, 3),
    ('Nikon Z30 Mirrorless Camera',    'Electronics',          55000, 64999,  15, 2),
    ('Philips Air Fryer HD9200',       'Electronics',           6000,  8499,  45, 5),
    ('Dyson V12 Vacuum Cleaner',       'Electronics',          35000, 42999,  20, 3),
    ('Mi Smart Air Purifier 4',        'Electronics',           8000, 10999,  35, 5),
    ('Havells 1.5 Ton AC',             'Electronics',          30000, 37999,  25, 3),
    ('Voltas 1.5 Ton Window AC',       'Electronics',          25000, 31999,  20, 3),

    # Mobile Phones
    ('iPhone 15 Pro Max 256GB',        'Mobile Phones',        120000,139999, 30, 3),
    ('iPhone 15 128GB',                'Mobile Phones',         75000, 89999, 40, 5),
    ('Samsung Galaxy S24 Ultra',       'Mobile Phones',         90000,109999, 25, 3),
    ('Samsung Galaxy A55',             'Mobile Phones',         28000, 34999, 50, 5),
    ('OnePlus 12 256GB',               'Mobile Phones',         55000, 64999, 35, 5),
    ('Redmi Note 13 Pro',              'Mobile Phones',         18000, 22999, 80, 8),
    ('Redmi 13C',                      'Mobile Phones',          8000, 10999,120,10),
    ('Realme 12 Pro+',                 'Mobile Phones',         25000, 29999, 45, 5),
    ('OPPO Reno 11',                   'Mobile Phones',         28000, 33999, 40, 5),
    ('Vivo V30 Pro',                   'Mobile Phones',         35000, 41999, 30, 5),
    ('Google Pixel 8',                 'Mobile Phones',         60000, 72999, 20, 3),
    ('Nothing Phone 2a',               'Mobile Phones',         22000, 26999, 35, 5),
    ('Motorola Edge 50 Pro',           'Mobile Phones',         30000, 35999, 30, 5),
    ('iQOO Neo 9 Pro',                 'Mobile Phones',         33000, 39999, 25, 5),

    # Laptops & Computers
    ('MacBook Air M3 13"',             'Laptops & Computers',  100000,119999, 20, 3),
    ('MacBook Pro M3 14"',             'Laptops & Computers',  160000,189999, 10, 2),
    ('Dell XPS 15',                    'Laptops & Computers',   90000,109999, 15, 2),
    ('HP Pavilion 15 i5',              'Laptops & Computers',   55000, 67999, 25, 3),
    ('Lenovo IdeaPad Slim 5',          'Laptops & Computers',   48000, 58999, 30, 3),
    ('ASUS ROG Zephyrus G14',          'Laptops & Computers',  110000,129999, 12, 2),
    ('Acer Aspire 7 Gaming',           'Laptops & Computers',   60000, 72999, 20, 3),
    ('Dell Inspiron 15 3000',          'Laptops & Computers',   40000, 48999, 35, 5),
    ('Logitech MX Master 3 Mouse',     'Laptops & Computers',    7000,  9499, 80, 8),
    ('Keychron K2 Keyboard',           'Laptops & Computers',    6500,  8999, 60, 5),
    ('Dell 27" 4K Monitor',            'Laptops & Computers',   30000, 36999, 20, 3),
    ('Samsung 1TB SSD',                'Laptops & Computers',    7000,  9499, 50, 5),
    ('Seagate 2TB HDD',                'Laptops & Computers',    4500,  5999, 60, 5),

    # Clothing
    ('Allen Solly Men Formal Shirt',   'Clothing',               800,  1499,  150,10),
    ('Raymond Men Suit',               'Clothing',              8000, 12999,   30, 5),
    ('Levi\'s 511 Slim Jeans',         'Clothing',              2000,  3499,  100,10),
    ('Peter England Formal Trousers',  'Clothing',              1200,  1999,   80, 8),
    ('Van Heusen Polo T-Shirt',        'Clothing',               600,   999,  200,15),
    ('H&M Women Dress',                'Clothing',              1500,  2499,  120,10),
    ('Zara Women Blazer',              'Clothing',              4000,  6499,   50, 5),
    ('W Women Kurta Set',              'Clothing',              1800,  2999,  100,10),
    ('Biba Anarkali Suit',             'Clothing',              2500,  3999,   80, 8),
    ('Fabindia Linen Saree',           'Clothing',              3500,  5499,   60, 5),
    ('Nike Dri-FIT T-Shirt',           'Clothing',              1200,  1999,  150,10),
    ('Adidas Joggers',                 'Clothing',              2000,  3299,  100,10),
    ('Puma Hoodie',                    'Clothing',              2500,  3999,   80, 8),

    # Footwear
    ('Nike Air Max 270',               'Footwear',              7000,  9999,   60, 5),
    ('Adidas Ultraboost 22',           'Footwear',              9000, 12999,   40, 5),
    ('Puma RS-X Sneakers',             'Footwear',              5000,  7499,   70, 5),
    ('Red Chief Leather Shoes',        'Footwear',              2500,  3999,   80, 8),
    ('Bata Men Formal Shoes',          'Footwear',              1800,  2999,  100,10),
    ('Metro Women Heels',              'Footwear',              1500,  2499,   90, 8),
    ('Woodland Men Boots',             'Footwear',              4000,  5999,   50, 5),
    ('Crocs Classic Clogs',            'Footwear',              2500,  3999,   80, 8),
    ('Sparx Running Shoes',            'Footwear',              1200,  1999,  120,10),

    # Food & Beverages
    ('Tata Tea Premium 500g',          'Food & Beverages',       200,   349,  200,20),
    ('Nescafe Classic Coffee 200g',    'Food & Beverages',       400,   599,  150,15),
    ('Amul Butter 500g',               'Food & Beverages',       250,   310,  200,20),
    ('Fortune Sunflower Oil 5L',       'Food & Beverages',       700,   899,  150,15),
    ('Aashirvaad Atta 10kg',           'Food & Beverages',       450,   599,  200,20),
    ('Maggi Noodles 12 Pack',          'Food & Beverages',       150,   240,  300,25),
    ('Bournvita 1kg',                  'Food & Beverages',       450,   620,  150,15),
    ('Horlicks 1kg',                   'Food & Beverages',       400,   580,  150,15),
    ('Lay\'s Chips Variety Pack',      'Food & Beverages',       200,   349,  250,20),
    ('Haldiram Namkeen Assorted',      'Food & Beverages',       300,   499,  200,20),
    ('Basmati Rice India Gate 5kg',    'Food & Beverages',       600,   849,  150,15),
    ('Toor Dal 5kg',                   'Food & Beverages',       500,   699,  150,15),
    ('Red Bull Energy Drink 4 Pack',   'Food & Beverages',       400,   599,  200,20),

    # Home & Kitchen
    ('Prestige Pressure Cooker 5L',    'Home & Kitchen',        1500,  2299,   80, 8),
    ('Milton Flask 1L',                'Home & Kitchen',         600,   999,  120,10),
    ('Borosil Glass Set 6pcs',         'Home & Kitchen',         800,  1299,  100,10),
    ('Pigeon Non-Stick Pan Set',       'Home & Kitchen',        1200,  1999,   80, 8),
    ('Cello Water Bottle 1L',          'Home & Kitchen',         200,   349,  200,20),
    ('Tupperware Lunch Box Set',       'Home & Kitchen',        1000,  1699,  100,10),
    ('Bajaj Mixer Grinder 750W',       'Home & Kitchen',        3000,  4499,   60, 5),
    ('Philips Induction Cooker',       'Home & Kitchen',        2500,  3799,   50, 5),
    ('Kent RO Water Purifier',         'Home & Kitchen',       12000, 16999,   25, 3),
    ('Usha Fan 1200mm',                'Home & Kitchen',        2000,  2999,   60, 5),

    # Furniture
    ('Nilkamal 3 Seater Sofa',         'Furniture',            18000, 24999,   15, 2),
    ('Wooden King Size Bed',           'Furniture',            25000, 34999,   10, 2),
    ('Study Table with Shelf',         'Furniture',             8000, 12999,   20, 3),
    ('Revolving Office Chair',         'Furniture',             6000,  9499,   30, 3),
    ('Shoe Rack 5 Tier',               'Furniture',             2500,  3999,   50, 5),
    ('Bookshelf 6 Shelf',              'Furniture',             5000,  7499,   30, 3),
    ('Dining Table 6 Seater',          'Furniture',            20000, 27999,   10, 2),
    ('Wardrobe 3 Door',                'Furniture',            18000, 24999,   12, 2),

    # Books
    ('Rich Dad Poor Dad',              'Books',                  200,   399,  200,20),
    ('Atomic Habits',                  'Books',                  250,   499,  150,15),
    ('The Alchemist',                  'Books',                  150,   299,  200,20),
    ('Wings of Fire - APJ Abdul Kalam','Books',                  180,   349,  200,20),
    ('Zero to One',                    'Books',                  300,   549,  100,10),
    ('Think and Grow Rich',            'Books',                  200,   399,  150,15),
    ('Python Programming O\'Reilly',   'Books',                  600,   999,  100,10),
    ('Clean Code',                     'Books',                  700,  1199,   80, 8),
    ('Data Structures Cormen',         'Books',                  800,  1299,   80, 8),
    ('NCERT Class 12 Physics',         'Books',                  150,   249,  300,25),

    # Sports & Fitness
    ('Cosco Football Size 5',          'Sports & Fitness',       600,   999,  100,10),
    ('Yonex Badminton Racket',         'Sports & Fitness',      1500,  2499,   80, 8),
    ('SG Cricket Bat English Willow',  'Sports & Fitness',      4000,  6499,   40, 5),
    ('Nivia Basketball',               'Sports & Fitness',       800,  1299,   80, 8),
    ('Decathlon Yoga Mat',             'Sports & Fitness',       600,   999,  120,10),
    ('Boldfit Resistance Bands Set',   'Sports & Fitness',       400,   699,  150,15),
    ('PowerBlock Adjustable Dumbbell', 'Sports & Fitness',      8000, 11999,   30, 3),
    ('Skipping Rope Steel',            'Sports & Fitness',       200,   399,  200,20),
    ('Protein Shaker Bottle',          'Sports & Fitness',       300,   549,  150,15),

    # Beauty & Personal Care
    ('Lakme Face Wash 100ml',          'Beauty & Personal Care', 150,   249,  200,20),
    ('Nivea Body Lotion 400ml',        'Beauty & Personal Care', 300,   499,  200,20),
    ('Himalaya Neem Face Pack',        'Beauty & Personal Care', 100,   199,  300,25),
    ('L\'Oreal Hair Shampoo 400ml',   'Beauty & Personal Care', 400,   649,  150,15),
    ('Dove Soap 4 Pack',              'Beauty & Personal Care', 200,   349,  250,20),
    ('Gillette Mach3 Razor',          'Beauty & Personal Care', 300,   549,  150,15),
    ('Park Avenue Perfume 100ml',     'Beauty & Personal Care', 600,   999,  100,10),
    ('Maybelline Lipstick',           'Beauty & Personal Care', 300,   549,  200,20),
    ('VLCC Face Cream SPF40',         'Beauty & Personal Care', 250,   449,  150,15),

    # Toys & Games
    ('LEGO Classic Brick Box',        'Toys & Games',           3000,  4999,   50, 5),
    ('Hot Wheels 20 Car Set',         'Toys & Games',           1000,  1699,  100,10),
    ('Funskool Monopoly',             'Toys & Games',           1200,  1999,   80, 8),
    ('Barbie Dreamhouse',             'Toys & Games',           8000, 12999,   20, 3),
    ('Remote Control Car',            'Toys & Games',           1500,  2499,   80, 8),
    ('Rubik\'s Cube 3x3',            'Toys & Games',            300,   599,  200,20),
    ('Carrom Board Full Size',        'Toys & Games',           2000,  3299,   60, 5),
    ('Chess Set Wooden',              'Toys & Games',            800,  1299,  100,10),
    ('Nerf Gun Blaster',              'Toys & Games',           1500,  2499,   80, 8),
]

# Insert all products
for name, cat, cost, sell, stock, reorder in products:
    cat_id = cat_ids.get(cat)
    if not cat_id:
        continue
    cursor.execute("""
        INSERT INTO products
        (product_name, category_id, cost_price, selling_price, stock_quantity, reorder_level)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, cat_id, cost, sell, stock, reorder))

conn.commit()
cursor.close()
conn.close()
print(f"✅ Successfully inserted {len(products)} products across {len(categories)} categories!")