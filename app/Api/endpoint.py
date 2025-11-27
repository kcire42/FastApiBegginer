from fastapi import FastAPI, HTTPException
import datetime
from app.Api.baseModel import CustomerBase, Transaction ,Invoice , Customer , CustomerCreate

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Message": "World"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/hour/{format}")
async def get_hour(format: int):
    formatTime = "%I:%M %p"
    if format == 24:
        formatTime = "%H:%M"    
    current_hour = datetime.datetime.now().time().strftime(formatTime)
    return {"current_hour": current_hour}

rank = {
    'S':'Sanin',
    'A':'Jounin',
    'B':'Chunin',
    'C':'Genin',
    'D':'Academy Student'
}

customer_db : list[Customer] = []

@app.get("/customers/")
async def get_customers():
    return customer_db

@app.get("/name/{name}/{years}/{rank_code}")
async def greet_name(name: str, years: int, rank_code: str):
    rank_full = rank.get(rank_code.upper(), "Unknown Rank")
    return {"greeting": f"Hello, {name}! You are {years} years old and your rank is {rank_full}."}

@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    for customer in customer_db:
        if customer.id == customer_id:
            return customer
    raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")

@app.post("/customers/")
async def create_customer(customer: CustomerCreate, response_model=Customer):
    new_customer = Customer(**customer.model_dump()) # conversion from CustomerCreate to Customer into a dictionary with the same params
    customer_db.append(new_customer)
    return new_customer

@app.post("/transactions")
async def create_transaction(transaction: Transaction):
    return transaction

@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice