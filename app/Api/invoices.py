from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session , joinedload
from app.Api.baseModel import Invoice , InvoiceOut 
from app.database.databaseConnection import getDB
from app.database.models import CustomerModel, TransactionModel, InvoiceModel
import datetime

invoice_router = APIRouter(prefix="/invoices",tags=["invoices"]) # routeur para la API de facturas


@invoice_router.get("/")
async def get_invoices(db : Session = Depends(getDB)):
    invoices = db.query(InvoiceModel).all()
    return invoices


@invoice_router.post("/",response_model=InvoiceOut)
async def create_invoice(invoice: Invoice, db : Session = Depends(getDB)):
    customer = db.query(CustomerModel).filter(CustomerModel.email == invoice.customer.email).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with email {invoice.customer.email} not found. Cannot create invoice.")
    dbInvoice = InvoiceModel(customer_id=customer.id)
    db.add(dbInvoice)
    db.flush()  # Usamos flush para obtener el ID antes de commit
    transaction_models = []
    for transaction in invoice.transaction:
        dbTransaction = TransactionModel(
            amount=transaction.amount,
            description=transaction.description,
            timestamp=datetime.datetime.now(),
            invoice_id=dbInvoice.id
        )
        transaction_models.append(dbTransaction)
    db.add_all(transaction_models)
    db.commit()
    db.refresh(dbInvoice)
    # Recarga las transacciones asociadas
    return dbInvoice


@invoice_router.get("/by_customer/{customer_id}")
async def get_invoices_by_customer(customer_id: int, db : Session = Depends(getDB)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).options(
        joinedload(CustomerModel.invoices).joinedload(InvoiceModel.transactions)
    ).all()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found.")
    return customer