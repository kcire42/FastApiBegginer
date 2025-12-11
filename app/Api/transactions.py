from fastapi import HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from app.Api.baseModel import Transaction
from app.database.databaseConnection import getDB
from app.database.models import TransactionModel, InvoiceModel
import datetime

transaction_router = APIRouter(prefix="/transactions",tags=["transactions"]) # routeur para la API de transacciones



@transaction_router.get("/")
async def get_transactions(db : Session = Depends(getDB), skip: int = Query(0,description="Number of records to skip"), limit: int = Query(10,description="Maximum number of records to return")):
    transactions = db.query(TransactionModel).offset(skip).limit(limit).all()
    return transactions


@transaction_router.post("/")
async def create_transaction(invoice_id: int, transaction: Transaction, db : Session = Depends(getDB)):
    invoice_exists = db.query(InvoiceModel).filter(InvoiceModel.id == invoice_id).first()
    if not invoice_exists:
        raise HTTPException(status_code=404, detail=f"Invoice with ID {invoice_id} not found. Cannot add transaction.")
    
    try:
        # 2. Crea la instancia del modelo de DB, usando el ID proporcionado
        dbTransaction = TransactionModel(
            amount=transaction.amount,
            description=transaction.description,
            timestamp=datetime.datetime.now(), 
            invoice_id=invoice_id # 💡 Asigna el ID de la ruta, no un valor fijo.
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en los datos de transacción: {e}")
    db.add(dbTransaction)
    db.commit()
    db.refresh(dbTransaction)
    return dbTransaction