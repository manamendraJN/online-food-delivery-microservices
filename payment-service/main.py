from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Payment, PaymentCreate, PaymentUpdate
from service import PaymentService

app = FastAPI(title="Payment Microservice", version="1.0.0")
payment_service = PaymentService()


@app.get("/")
def read_root():
    return {"message": "Payment Microservice is running"}


@app.get("/api/payments", response_model=List[Payment])
def get_all_payments():
    try:
        return payment_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve payments: {str(e)}")


@app.get("/api/payments/{payment_id}", response_model=Payment)
def get_payment(payment_id: int):
    try:
        payment = payment_service.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment with ID {payment_id} not found")
        return payment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve payment: {str(e)}")


@app.post("/api/payments", response_model=Payment, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate):
    try:
        return payment_service.create(payment)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create payment: {str(e)}")


@app.put("/api/payments/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, payment: PaymentUpdate):
    try:
        updated_payment = payment_service.update(payment_id, payment)
        if not updated_payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment with ID {payment_id} not found")
        return updated_payment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update payment: {str(e)}")


@app.delete("/api/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int):
    try:
        success = payment_service.delete(payment_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment with ID {payment_id} not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete payment: {str(e)}")
