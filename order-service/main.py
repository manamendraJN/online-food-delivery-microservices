from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Order, OrderCreate, OrderUpdate
from service import OrderService

app = FastAPI(title="Order Microservice", version="1.0.0")
order_service = OrderService()


@app.get("/")
def read_root():
    return {"message": "Order Microservice is running"}


@app.get("/api/orders", response_model=List[Order])
def get_all_orders():
    try:
        return order_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve orders: {str(e)}")


@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    try:
        order = order_service.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {order_id} not found")
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve order: {str(e)}")


@app.post("/api/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    try:
        return order_service.create(order)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create order: {str(e)}")


@app.put("/api/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: OrderUpdate):
    try:
        updated_order = order_service.update(order_id, order)
        if not updated_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {order_id} not found")
        return updated_order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update order: {str(e)}")


@app.delete("/api/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int):
    try:
        success = order_service.delete(order_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {order_id} not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete order: {str(e)}")
