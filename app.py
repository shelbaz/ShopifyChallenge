from flask import Flask, request, json, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
import contextlib
from sqlalchemy import MetaData

from flask_graphql import GraphQLView
# from schema import schema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

session = db.session

## Database Models

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    shopping_cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float)
    user_id = db.Column(db.Integer)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float)
    user_id = db.Column(db.Integer)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    shopping_cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'))
    shopping_cart = db.relationship(ShoppingCart, cascade="delete, delete-orphan", single_parent=True)


# app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

# default_query = '''
# {
#   allProducts {
#     edges {
#       node {
#         id,
#         title,
#         quantity,
#         price
#         }
#     }
#   }
# }

@app.route('/')
def index():
	return "Go to /graphql"


@app.route('/product/', methods=['GET'])
def get_all_products():
    """
           GET request for all products
           :returns: JSON of products
           - Example
           .. code-block:: JSON
            {
                "data": [
                    {
                        "id": 1,
                        "price": 1200,
                        "quantity": 10,
                        "title": "Macbook"
                    },
                    {
                        "id": 2,
                        "price": 1800,
                        "quantity": 5,
                        "title": "Macbook Pro"
                    },
                    {
                        "id": 3,
                        "price": 800,
                        "quantity": 10,
                        "title": "iPad"
                    }
                ]
            }
           """

    products = Product.query.all()
    product_list = []
    for product in products:
        product_details = {'id': product.id, 'title': product.title, 'price': product.price,
                         'quantity': product.quantity}
        product_list.append(product_details)
    return jsonify({'data': product_list})

@app.route('/product/in_stock', methods=['GET'])
def get_instock_products():
    """
       GET request for all products whose quantity is greater than 0
       :returns: JSON of products
       - Example
       .. code-block:: JSON
        {
            "data": [
                {
                    "id": 1,
                    "price": 1200,
                    "quantity": 10,
                    "title": "Macbook"
                },
                {
                    "id": 2,
                    "price": 1800,
                    "quantity": 5,
                    "title": "Macbook Pro"
                },
                {
                    "id": 3,
                    "price": 800,
                    "quantity": 10,
                    "title": "iPad"
                }
            ]
        }
       """

    products = Product.query.filter(Product.quantity> 0)
    product_list = []
    for product in products:
        product_details = {'id': product.id, 'price': product.price,
                         'quantity': product.quantity}
        product_list.append(product_details)
    return jsonify({'data': product_list})


@app.route('/product/add', methods=['GET', 'POST'])
def create_product():
    """
       Create a new product or adds stock to the product if it already exists
       :returns: Status of product creation
       - Example
       .. code-block:: JSON
           {
                "title": "Macbook",
                "price": 1000.10,
                "quantity": 5
            }
       """
    try:
        json_obj = request.get_json()
        print(json_obj, flush=True)
        result = Product.query.filter_by(title=json_obj['title']).first()

        if not result:
            new = Product(title=json_obj['title'], price=json_obj['price'], quantity=json_obj['quantity'])
            session.add(new)
            session.commit()
            return jsonify({'status': 'New product successfully added'}), 201

        else:
            result.quantity += json_obj['quantity']
            session.commit()
            return jsonify({'status': 'Existing product. Stock has been added'}), 201
    except:
        return jsonify({'status': 'An error occurred, product could not be added'}), 404


@app.route('/cart/create', methods=['GET'])
def create_cart():
    """
       Create a new cart, .
       :returns: Cart model object

    """
    new_cart = ShoppingCart()
    session.add(new_cart)
    session.commit()
    return new_cart

@app.route('/user/create', methods=['POST', 'GET'])
def create_user():
    """
       Create a user, and his cart associated with him.
       :returns: Status of user creation
       - Example
       .. code-block:: JSON
           {
                "username": "shelbaz",
                "password": "abs241",
                "email": "shaw1n@gmail.com"
            }
       """
    json_obj = request.get_json()
    print(json_obj, flush=True)
    cart = create_cart()
    print("cart id:" + str(cart.id))
    email, username, password = json_obj['email'], json_obj['username'], json_obj['password']
    new_user = User(email=email, username=username, password=password, shopping_cart_id=cart.id)
    print(new_user)
    try:
        session.add(new_user)
        session.commit()
        setattr(cart, 'user_id', new_user.id)
        session.commit()
        return jsonify({'status': 'User id: ' + str(new_user.id) + ' created successfully , cart-id:' + str(new_user.shopping_cart_id)}), 201
    except:
        return jsonify({'status': 'An error occurred, user could not be added'}), 404

@app.route('/cart/add/<userid>', methods=['POST', 'GET'])
def add_to_cart(userid):

    """
    Add items to cart, passing the item id and quantities as JSON.
    :param str userid: ID of the user
    :returns: Status of cart
    - Example
    .. code-block:: JSON
        {
            "products": [
                {
                    "id": 1,
                    "quantity": 1
                },
                {
                    "id": 2,
                    "quantity": 2
                },
                {
                    "id": 3,
                    "quantity": 1
                }
                      ]
        }
    """


    json_obj = request.get_json()
    product_array = json_obj['products']

    print(product_array, flush=True)
    user = get_user(userid)
    print(user)

    total_price = 0
    cart_array = [] ## ids of the  cart line items

    for product in product_array:
        print(product, flush=True)
        item = get_product(product['id'])
        cart_item = CartItem(name=item.title, quantity=item.quantity, price=item.price, product_id=item.id, shopping_cart_id=user.shopping_cart_id)
        total_price += item.price
        cart_array.append(cart_item.id)
        session.add(cart_item)
        session.commit()

    shopping_cart = get_cart(user.shopping_cart_id)
    setattr(shopping_cart, 'user_id', user.id)
    setattr(shopping_cart, 'total_price', total_price)
    session.commit()
    return jsonify({'status': 'Products added to cart of user: ' + str(userid)})


def get_user(userid):
    """
       Gets the user object assocated with the userid.
       :param str userid: ID of the user
       :returns: User Object

    """
    user = User.query.filter_by(id=userid).first()
    return user

def get_product(productid):
    """
       Gets the product object assocated with the productid.
       :param str productid: ID of the product
       :returns: Product Object

    """
    product = Product.query.filter_by(id=productid).first()
    return product

def get_cart(cartid):
    """
       Gets the cart object assocated with the cartid.
       :param str cartid: ID of the cartid
       :returns: Cart Object

    """
    cart = ShoppingCart.query.filter_by(id=cartid).first()
    return cart

def get_order(orderid):
    """
       Gets the order object assocated with the orderid.
       :param str orderid: ID of the order
       :returns: Order Object

    """
    order = Order.query.filter_by(id=orderid).first()
    return order

def seed_db():
    """
           Seed for the database to have initial products and users with associated carts
    """

    macbook = Product(title="Macbook", price=1200.00, quantity=10)
    macbook_pro = Product(title="Macbook Pro", price=1800.00, quantity=5)
    ipad = Product(title="iPad", price=800.00, quantity=10)
    ipad_pro = Product(title="iPad Pro", price=1200.00, quantity=0)
    iphone = Product(title="iPhone X", price=2000.00, quantity=10)

    session.add(macbook)
    session.add(macbook_pro)
    session.add(ipad)
    session.add(ipad_pro)
    session.add(iphone)

    cartA = ShoppingCart(user_id=1)
    cartB = ShoppingCart(user_id=2)
    cartC = ShoppingCart(user_id=3)

    session.add(cartA)
    session.add(cartB)
    session.add(cartC)

    session.commit()

    admin = User(email="admin@store.com", username="admin", password="admin", shopping_cart_id=cartA.id)
    superuser = User(email="superuser@store.com", username="superuser", password="superuser", shopping_cart_id=cartB.id)
    shopper = User(email="shopper@admin.com", username="shopper", password="shopper", shopping_cart_id=cartC.id)

    session.add(admin)
    session.add(superuser)
    session.add(shopper)

    print('adding stuff', flush=True)
    session.commit()

def create_db():
    db.create_all()

def clear_db():
    meta = MetaData()
    meta.drop_all()

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

if __name__ == '__main__':
    try:
        clear_db()
    except:
        create_db()
    seed_db()
    app.run()

