from fastapi import FastAPI
from app.database.databaseConnection import createDBTable
from app.database import models  # Asegura que los endpoints se registren
from app.Api.general import general_router as general_router
from app.Api.customers import customer_router as customer_router
from app.Api.invoices import invoice_router as invoice_router
from app.Api.transactions import transaction_router as transaction_router

app = FastAPI()

app.include_router(router=general_router)
app.include_router(router=customer_router)
app.include_router(router=invoice_router)
app.include_router(router=transaction_router)

@app.on_event("startup")
def on_startup():
    """Evento que se ejecuta al iniciar la aplicación FastAPI."""
    createDBTable()
    print("Database tables created on startup.")


