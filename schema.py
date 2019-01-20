import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType, utils
from models import Product as ProductModel
from models import ShoppingCart as ShoppingCartModel
from models import CartItem as CartItemModel
from models import Order as OrderModel

class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel
        interfaces = (relay.Node, )

class ProductConnection(relay.Connection):
    class Meta:
        node = Product



class ShoppingCart(SQLAlchemyObjectType):
    class Meta:
        model = ShoppingCartModel
        interfaces = (relay.Node, )

class ShoppingCartConnection(relay.Connection):
    class Meta:
        node = ShoppingCart



class CartItem(SQLAlchemyObjectType):
    class Meta:
        model = CartItemModel
        interfaces = (relay.Node, )

class CartItemConnection(relay.Connection):
    class Meta:
        node = CartItem



class Order(SQLAlchemyObjectType):
    class Meta:
        model = OrderModel
        interfaces = (relay.Node, )

class OrderConnection(relay.Connection):
    class Meta:
        node = Order


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_products = SQLAlchemyConnectionField(ProductConnection)
    all_shopping_carts = SQLAlchemyConnectionField(ShoppingCartConnection)
    all_cart_items = SQLAlchemyConnectionField(CartItemConnection)
    all_orders = SQLAlchemyConnectionField(OrderConnection)


schema = graphene.Schema(query=Query, types=[Product, ShoppingCart, CartItem, Order])