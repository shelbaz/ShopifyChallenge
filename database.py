from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import Order, ShoppingCart, CartItem, Product

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    macbook = Product(title="Macbook", price=1200.00, quantity=10)
    macbook_pro = Product(title="Macbook Pro", price=1800.00, quantity=10)
    ipad = Product(title="iPad", price=800.00, quantity=10)
    ipad_pro = Product(title="iPad Pro", price=1200.00, quantity=10)
    iphone = Product(title="iPhone X", price=2000.00, quantity=10)

    db_session.add(macbook)
    db_session.add(macbook_pro)
    db_session.add(ipad)
    db_session.add(ipad_pro)
    db_session.add(iphone)

    db_session.commit()


