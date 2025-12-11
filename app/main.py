from fastapi import FastAPI, Request
from app.database.databaseConnection import createDBTable
from app.database import models  # Asegura que los endpoints se registren
from app.Api.general import general_router as general_router
from app.Api.customers import customer_router as customer_router
from app.Api.invoices import invoice_router as invoice_router
from app.Api.transactions import transaction_router as transaction_router
import logging

app = FastAPI()

app.include_router(router=general_router)
app.include_router(router=customer_router)
app.include_router(router=invoice_router)
app.include_router(router=transaction_router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware para procesar cada solicitud HTTP."""
    logger = logging.getLogger("uvicorn.access")
    response = await call_next(request)
    logger.info(f"Request: {request.method} {request.url} - Response status: {response.status_code}")
    return response


@app.on_event("startup")
def on_startup():
    """Evento que se ejecuta al iniciar la aplicación FastAPI."""
    createDBTable()
    print("Database tables created on startup.")


