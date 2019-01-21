# import graphene
# from graphene import relay
# from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType, utils
# from models import Product as ProductModel
# from models import ShoppingCart as ShoppingCartModel
# from models import CartItem as CartItemModel
# from models import Order as OrderModel
# from models import User as UserModel
# from app import session as db_session
#
#
# class Product(SQLAlchemyObjectType):
#     class Meta:
#         model = ProductModel
#         interfaces = (relay.Node, )
#
# class ProductConnection(relay.Connection):
#     class Meta:
#         node = Product
#
#
#
# class ShoppingCart(SQLAlchemyObjectType):
#     class Meta:
#         model = ShoppingCartModel
#         interfaces = (relay.Node, )
#
# class ShoppingCartConnection(relay.Connection):
#     class Meta:
#         node = ShoppingCart
#
#
#
# class CartItem(SQLAlchemyObjectType):
#     class Meta:
#         model = CartItemModel
#         interfaces = (relay.Node, )
#
# class CartItemConnection(relay.Connection):
#     class Meta:
#         node = CartItem
#
#
#
# class Order(SQLAlchemyObjectType):
#     class Meta:
#         model = OrderModel
#         interfaces = (relay.Node, )
#
# class OrderConnection(relay.Connection):
#     class Meta:
#         node = Order
#
# class User(SQLAlchemyObjectType):
#     class Meta:
#         model = UserModel
#         interfaces = (relay.Node, )
#
# class UserConnection(relay.Connection):
#     class Meta:
#         node = User
#
# class createUser(graphene.Mutation):
# 	class Input:
# 		name = graphene.String()
# 		email = graphene.String()
# 		username = graphene.String()
# 	ok = graphene.Boolean()
# 	user = graphene.Field(User)
#
# 	@classmethod
# 	def mutate(cls, _, args, context, info):
# 		user = UserModel(name=args.get('name'), email=args.get('email'), username=args.get('username'))
# 		db_session.add(user)
# 		db_session.commit()
# 		ok = True
# 		return createUser(user=user, ok=ok)
#
#
# class Query(graphene.ObjectType):
#     node = relay.Node.Field()
#     find_user = graphene.Field(lambda: User, username=graphene.String())
#     all_products = SQLAlchemyConnectionField(ProductConnection)
#     all_shopping_carts = SQLAlchemyConnectionField(ShoppingCartConnection)
#     all_cart_items = SQLAlchemyConnectionField(CartItemConnection)
#     all_orders = SQLAlchemyConnectionField(OrderConnection)
#     all_users = SQLAlchemyConnectionField(UserConnection)
#
#     def resolve_find_user(self, args, context, info):
#         query = User.get_query(context)
#         username = args.get('username')
#         # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
#         return query.filter(UserModel.username == username).first()
#
# class MyMutations(graphene.ObjectType):
# 	create_user = createUser.Field()
#
# schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Product, ShoppingCart, CartItem, Order, User])