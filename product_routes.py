from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import get_db_connection, log_activity

product_bp = Blueprint('product', __name__)

@product_bp.route('/product', methods=['GET', 'POST'])
def product_page():
    error_message = None
    
    if request.method == 'POST':
        if 'product_name' in request.form:
            error_message = add_product(request.form['product_name'])
        elif 'remove_product' in request.form:
            error_message = remove_product(request.form['product_to_remove'])
    
    products = get_all_products()
    
    return render_template('product.html', products=products, error_message=error_message)

def add_product(product_name):
    with get_db_connection() as conn:
        c = conn.cursor()
        
        # Check if the product already exists and is not removed
        c.execute('SELECT id, removed FROM products WHERE name = ?', (product_name,))
        existing_product = c.fetchone()
        
        if existing_product:
            if existing_product['removed']:
                # If the product is removed, reactivate it
                c.execute('UPDATE products SET removed = 0 WHERE id = ?', (existing_product['id'],))
                log_activity(f'add {product_name}')  # Log activity for reactivation
            else:
                return "Product name must be unique."
        else:
            # Add new product
            c.execute('INSERT INTO products (name, removed) VALUES (?, 0)', (product_name,))
            log_activity(f'add {product_name}')  # Log activity for adding a new product
        
        conn.commit()
    return None  # No error

def remove_product(product_to_remove):
    with get_db_connection() as conn:
        c = conn.cursor()
        
        c.execute('SELECT id, name FROM products WHERE name = ?', (product_to_remove,))
        existing_product = c.fetchone()
        
        if existing_product:
            # Remove the product by setting its status to removed
            c.execute('UPDATE products SET removed = 1 WHERE id = ?', (existing_product['id'],))
            conn.commit()
            log_activity(f'remove {existing_product["name"]}')  # Log activity for removal
        else:
            return "Product not found."
    
    return None  # No error

def get_all_products():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT id, name, removed FROM products')
        return c.fetchall()
