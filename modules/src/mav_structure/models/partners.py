from sqlalchemy import Column, DateTime, Integer, ForeignKey, UUID, String, Date, Boolean, Float
from sqlalchemy.orm import relationship

from .common import Base


class Partner(Base):
    __tablename__ = 'partners'

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String)
    phone = Column(String)
    username = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String)
    date_of_birth = Column(Date, nullable=True)
    salary = Column(Integer)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True))
    completed_signup_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships


class PartnerChatbotProfile(Base):
    __tablename__ = 'partner_chatbot_profile'
    __timestamps__ = ('created_at', 'updated_at', 'deleted_at',)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    partner_id = Column(UUID(as_uuid=True), ForeignKey('partners.uuid'), nullable=False)

    # Relationships
    partner = relationship('Partner', backref='chatbot_profile')


# ---------------------------------------- tables for DataEngineer interview purpose ----------


# Define the customers table
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)


# Define the stores table
class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String, nullable=False)


# Define the products table
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)


# Define the sales_transactions table
class SalesTransaction(Base):
    __tablename__ = 'sales_transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    sale_amount = Column(Float, nullable=False)
    transaction_date = Column(Date, nullable=False)

    customer = relationship("Customer")
    store = relationship("Store")
    product = relationship("Product")
