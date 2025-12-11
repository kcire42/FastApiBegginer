from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Clase base de la que heredarán todas las tabla
base = declarative_base()


class CustomerModel(base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    invoices = relationship("InvoiceModel", back_populates="customer")

class InvoiceModel(base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    transactions = relationship("TransactionModel", back_populates="invoice")
    customer = relationship("CustomerModel", back_populates="invoices")

class TransactionModel(base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    invoice = relationship("InvoiceModel", back_populates="transactions")