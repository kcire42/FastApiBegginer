from pydantic import BaseModel, EmailStr, computed_field
from typing import Union

class CustomerBase(BaseModel):
    name: str
    description: str 
    age: int
    email: EmailStr
    
    @computed_field
    @property
    def id(self) -> int:
        return hash(self.email) % 10000

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    
    pass

class Transaction(BaseModel):
    id: int
    amount: float
    description: str
    timestamp: str

class Invoice(BaseModel):
    id: int
    customer: CustomerBase
    transaction: list[Transaction]

    @computed_field
    @property
    def total_amount(self) -> float:
        return sum(transaction.amount for transaction in self.transaction)
    


    
