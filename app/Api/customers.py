from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.Api.baseModel import CustomerBase, Customer , CustomerCreate
from app.Api.security import verify_api_token
from app.database.databaseConnection import getDB
from app.database.models import CustomerModel



customer_router = APIRouter(prefix="/customers", tags=["customers"]) # routeur para la API de clientes

@customer_router.get("/")
async def get_customers(db : Session = Depends(getDB)):
    customers = db.query(CustomerModel).all()
    return customers


@customer_router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, db : Session = Depends(getDB)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")
    return customer

@customer_router.post("/")
async def create_customer(customer: CustomerCreate, db : Session = Depends(getDB), auth_token: str = Depends(verify_api_token)):
    dbCustomer = CustomerModel(**customer.model_dump())
    db.add(dbCustomer)
    db.commit()
    db.refresh(dbCustomer)
    return dbCustomer


@customer_router.delete("/{customer_id}")
async def delete_customer(customer_id: int, db : Session = Depends(getDB), auth_token: str = Depends(verify_api_token)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")
    db.delete(customer)
    db.commit()
    return {"detail": f"Customer with ID {customer_id} deleted"}

@customer_router.patch("/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_update: CustomerBase, db : Session = Depends(getDB), auth_token: str = Depends(verify_api_token)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")
    for key, value in customer_update.model_dump().items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer