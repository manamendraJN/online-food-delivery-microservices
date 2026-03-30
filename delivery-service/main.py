from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Delivery, DeliveryCreate, DeliveryUpdate
from service import DeliveryService

app = FastAPI(title="Delivery Microservice", version="1.0.0")
delivery_service = DeliveryService()


@app.get("/")
def read_root():
    return {"message": "Delivery Microservice is running"}


@app.get("/api/deliveries", response_model=List[Delivery])
def get_all_deliveries():
    try:
        return delivery_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve deliveries: {str(e)}")


@app.get("/api/deliveries/{delivery_id}", response_model=Delivery)
def get_delivery(delivery_id: int):
    try:
        delivery = delivery_service.get_by_id(delivery_id)
        if not delivery:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Delivery with ID {delivery_id} not found")
        return delivery
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve delivery: {str(e)}")


@app.post("/api/deliveries", response_model=Delivery, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliveryCreate):
    try:
        return delivery_service.create(delivery)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create delivery: {str(e)}")


@app.put("/api/deliveries/{delivery_id}", response_model=Delivery)
def update_delivery(delivery_id: int, delivery: DeliveryUpdate):
    try:
        updated_delivery = delivery_service.update(delivery_id, delivery)
        if not updated_delivery:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Delivery with ID {delivery_id} not found")
        return updated_delivery
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update delivery: {str(e)}")


@app.delete("/api/deliveries/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(delivery_id: int):
    try:
        success = delivery_service.delete(delivery_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Delivery with ID {delivery_id} not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete delivery: {str(e)}")
