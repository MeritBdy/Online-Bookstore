from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flaskext.mysql import MySQL
from functools import wraps

app = Flask(__name__)

# --- 1. CONFIGURATION ---
app.config['SECRET_KEY'] = 'dev-secret-key-12345'
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "bookstream_db" 

# --- 2. INITIALIZE ---
csrf = CSRFProtect(app)
mysql = MySQL(app)

# --- 3. FORMS ---
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Join the Collection")

# --- 4. DECORATORS ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("Unauthorized! Admin rights required.", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# --- 5. PUBLIC ROUTES ---

@app.route("/")
def index():
    search_query = request.args.get('search')
    conn = mysql.connect()
    cursor = conn.cursor()
    
    if search_query:
        # Search logic: Title or Author matches search query
        query = "SELECT id, title, author, price, image_url, description FROM books WHERE title LIKE %s OR author LIKE %s"
        cursor.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("SELECT id, title, author, price, image_url, description FROM books")
        
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", books=books)

@app.route("/book/<int:book_id>")
def book_details(book_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, price, image_url, description FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    if book:
        return render_template("details.html", book=book)
    flash("Book not found!", "danger")
    return redirect(url_for('index'))

# --- 6. AUTH ROUTES ---

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO user (full_name, email, password, role) VALUES (%s, %s, %s, 'user')", 
                           (form.full_name.data, form.email.data, form.password.data))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, role FROM user WHERE email = %s AND password = %s", 
                       (form.email.data, form.password.data))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session.update({'user_id': user[0], 'user_name': user[1], 'role': user[2], 'cart': []})
            flash(f"Welcome back, {user[1]}!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)

# --- 7. DASHBOARD & ADMIN ACTIONS ---

@app.route("/dashboard")
@login_required
def dashboard():
    search_query = request.args.get('search')
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Dashboard search functionality for both Books and Orders
    if search_query:
        cursor.execute("SELECT id, title, author, price, image_url, description FROM books WHERE title LIKE %s OR author LIKE %s", 
                       ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("SELECT id, title, author, price, image_url, description FROM books")
    
    books = cursor.fetchall()
    
    # Get Orders based on Role
    if session.get('role') == 'admin':
        cursor.execute("""
            SELECT o.id, b.title, o.total_price, o.created_at, u.full_name 
            FROM orders o 
            JOIN books b ON o.book_id = b.id 
            JOIN user u ON o.user_id = u.id
            ORDER BY o.created_at DESC
        """)
    else:
        cursor.execute("""
            SELECT o.id, b.title, o.total_price, o.created_at 
            FROM orders o 
            JOIN books b ON o.book_id = b.id 
            WHERE o.user_id = %s
            ORDER BY o.created_at DESC
        """, (session['user_id'],))
    
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("dashboard.html", books=books, orders=orders)

@app.route("/add_book", methods=["POST"])
@login_required
@admin_only
def add_book():
    data = (
        request.form.get('title'), 
        request.form.get('author'), 
        request.form.get('price'), 
        request.form.get('image_url'),
        request.form.get('description')
    )
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, price, image_url, description) VALUES (%s, %s, %s, %s, %s)", data)
    conn.commit()
    cursor.close()
    conn.close()
    flash("Book added to collection!", "success")
    return redirect(url_for('dashboard'))

@app.route("/edit_book/<int:book_id>", methods=["POST"])
@login_required
@admin_only
def edit_book(book_id):
    data = (
        request.form.get('title'), 
        request.form.get('author'), 
        request.form.get('price'), 
        request.form.get('image_url'), 
        request.form.get('description'),
        book_id
    )
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=%s, author=%s, price=%s, image_url=%s, description=%s WHERE id=%s", data)
    conn.commit()
    cursor.close()
    conn.close()
    flash("Book updated!", "success")
    return redirect(url_for('dashboard'))

@app.route("/delete_book/<int:book_id>")
@login_required
@admin_only
def delete_book(book_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Book removed.", "info")
    return redirect(url_for('dashboard'))


@app.route("/delete_order/<int:order_id>", methods=["POST"])
@login_required
@admin_only
def delete_order(order_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        conn.commit()
        flash(f"Transaction #{order_id} has been removed from history.", "info")
    except Exception as e:
        flash(f"Error deleting record: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('dashboard'))

# --- 8. CART & USER ACTIONS ---

@app.route("/add_to_cart/<int:book_id>")
@login_required
def add_to_cart(book_id):
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    cart.append(book_id)
    session['cart'] = cart
    session.modified = True 
    flash("Added to cart!", "success")
    return redirect(url_for('dashboard'))

@app.route("/cart")
@login_required
def view_cart():
    if not session.get('cart'):
        flash("Cart is empty!", "info")
        return redirect(url_for('dashboard'))
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    placeholders = ', '.join(['%s'] * len(session['cart']))
    cursor.execute(f"SELECT id, title, author, price, image_url FROM books WHERE id IN ({placeholders})", tuple(session['cart']))
    cart_items = cursor.fetchall()
    
    total = sum(item[3] for item in cart_items)
    cursor.close()
    conn.close()
    return render_template("cart.html", items=cart_items, total=total)

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if not session.get('cart'):
        flash("Your cart is empty!", "warning")
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        payment_method = request.form.get('payment_method')
        user_id = session['user_id']
        conn = mysql.connect()
        cursor = conn.cursor()
        
        try:
            for book_id in session['cart']:
                cursor.execute("SELECT price FROM books WHERE id = %s", (book_id,))
                price_data = cursor.fetchone()
                if price_data:
                    price = price_data[0]
                    cursor.execute("INSERT INTO orders (user_id, book_id, total_price) VALUES (%s, %s, %s)", 
                                   (user_id, book_id, price))
            
            conn.commit()
            session.pop('cart', None) 
            flash(f"Order successful via {payment_method}! Check your dashboard.", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Transaction failed: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template("payment.html")

@app.route("/remove_from_cart/<int:book_id>")
@login_required
def remove_from_cart(book_id):
    if 'cart' in session:
        cart = session['cart']
        if book_id in cart:
            cart.remove(book_id) 
            session['cart'] = cart
            session.modified = True
            flash("Book removed from cart.", "info")
    return redirect(url_for('view_cart'))

@app.route("/clear_cart")
def clear_cart():
    session.pop('cart', None)
    flash("Cart cleared.", "info")
    return redirect(url_for('dashboard'))


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=8000)