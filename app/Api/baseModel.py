from pydantic import BaseModel, EmailStr, computed_field
from typing import Union
import datetime

class CustomerBase(BaseModel):
    name: str
    description: str 
    age: int
    email: EmailStr
    
    # @computed_field
    # @property
    # def id(self) -> int:
    #     return hash(self.email) % 10000

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id : int
    class Config:
        from_attributes = True

class Transaction(BaseModel):
    amount: float
    description: str
    timestamp: datetime.datetime

# Modelo de SALIDA (Output) de una Transacción
class TransactionOut(Transaction):
    id: int
    invoice_id: int # Necesario para mostrar la clave foránea
    
    class Config:
        from_attributes = True

class Invoice(BaseModel):
    customer: CustomerBase
    transaction: list[Transaction]


    
# Modelo de SALIDA (Output) de una Factura
class InvoiceOut(BaseModel):
    id: int
    customer: Customer # Usamos Customer (con ID)
    # Usamos TransactionOut para la lista de transacciones (con IDs)
    transactions: list[TransactionOut]
    
    class Config:
        # Nota: El campo "transaction" en la entrada Pydantic se mapea 
        # automáticamente a "transactions" en el modelo de salida de SQLAlchemy (models.py)
        from_attributes = True


    
