# uv add flask flask-sqlalchemy flask-bcrypt run to install flask
from flask import Flask, jsonify, request
from models import Product, bcrypt, db, User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  
bcrypt.init_app(app)  

with app.app_context():
    db.create_all()

# check if the flask is running or installed correctly
@app.route('/')
def home():
    return "Flask is running"

# register func
@app.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'email and password are required'}),400
    
    if User.query.filter_by(email = email).first():
        return jsonify({'message': 'User already exists'}),400

    user = User(email = email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User Registered Successfully'})



@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not email or not password:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify(
        {
            'message': 'Login Successfull',
            'user': {
                'id': user.id,
                'email': user.email
            }
        }
    ), 200



# ================== PRODUCT ROUTES ==================


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    required_field = ["name", "brand", "category", "gender", "images", "selling_price"]

    for field in required_field:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    product = Product(
        name=data["name"],
        brand=data["brand"],
        category=data["category"],
        gender=data["gender"],
        description=data.get("description"),
        images=",".join(data["images"]),
        selling_price=data["selling_price"],
        discount=data.get("discount", 0.0),
        average_rating=data.get("average_rating", 0.0),
        total_reviews=data.get("total_reviews", 0),
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(
        {"message": "Product added successfully", "product": product.to_dict()}
    ), 201


@app.route("/products", methods=["PUT"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    product.name = data.get("name", product.name)
    product.brand = data.get("brand", product.brand)
    product.category = data.get("category", product.category)
    product.gender = data.get("gender", product.gender)
    product.description = data.get("description", product.description)
    product.selling_price = data.get("selling_price", product.selling_price)
    product.discount = data.get("discount", product.discount)
    product.average_rating = data.get("average_rating", product.average_rating)
    product.total_reviews = data.get("total_reviews", product.total_reviews)

    if "images" in data:
        product.images = ",".join(data["images"])

    db.session.commit()

    return jsonify(
        {"message": "Product updated successfully", "product": product.to_dict()}
    ), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 5000)