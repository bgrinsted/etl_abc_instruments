from sqlalchemy import ForeignKey, func
from sqlalchemy import Column, String, Integer, Float, Date, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    date_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Product(Base):
    __tablename__ = "dim_product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(30))
    Type = Column(String(30))
    UnitPrice = Column(Float)


class Payment(Base):
    __tablename__ = "dim_payment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    BillingCode = Column(String(20))
    Type = Column(String(10))
    Date = Column(Date)


class Client(Base):
    __tablename__ = "dim_client"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(120))


class Delivery(Base):
    __tablename__ = "dim_delivery"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Address = Column(String(120))
    City = Column(String(40))
    Postcode = Column(String(10))
    Country = Column(String(50))
    ContactNumber = Column(String(25))


class FactOrderItem(Base):
    __tablename__ = "fact_order_item"
    id = Column(Integer, primary_key=True, autoincrement=True)
    OrderNumber = Column(String(15), unique=True)
    Quantity = Column(Integer)
    TotalPrice = Column(Float)
    Currency = Column(String(3))

    ProductId = Column(Integer, ForeignKey("dim_product.id"))
    dim_product = relationship(Product)

    PaymentId = Column(Integer, ForeignKey("dim_payment.id"))
    dim_payment = relationship(Payment)

    ClientId = Column(Integer, ForeignKey("dim_client.id"))
    dim_client = relationship(Client)

    DeliveryId = Column(Integer, ForeignKey("dim_delivery.id"))
    dim_delivery = relationship(Delivery)
