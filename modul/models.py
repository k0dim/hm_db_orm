from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True)


class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=100), unique=True)
    id_publisher = Column(Integer, ForeignKey("publisher.id"), nullable=False)
    course = relationship(Publisher, backref="book")


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey("book.id"), nullable=False)
    id_shop = Column(Integer, ForeignKey("shop.id"), nullable=False)
    count = Column(Integer, nullable=False)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")


class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True)
    price = Column(Numeric, nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey("stock.id"), nullable=False)
    count = Column(Integer, nullable=False)
    stock = relationship(Stock, backref="sale")

# Создать таблицы
def create_tables(engine):
    Base.metadata.create_all(engine)

# Удалить таблицы
def drop_tables(engine):
    Base.metadata.drop_all(engine)
