from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/<username>')
def user_profile(username):
    return render_template('user_profile.html', username=username)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    # In a real app, you'd fetch product details from a database
    products = {
        1: {"name": "Laptop", "price": 999.99},
        2: {"name": "Smartphone", "price": 499.99},
        3: {"name": "Tablet", "price": 299.99}
    }
    product = products.get(product_id, {"name": "Unknown", "price": 0})
    return render_template('product_details.html', product_id=product_id, product=product)

if __name__ == '__main__':
    app.run(debug=True)