from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
from typing import Any, Optional, List

app = FastAPI(title="Food Delivery API Gateway", version="1.0.0")


class UserCreate(BaseModel):
    name: str
    email: str
    phone: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class RestaurantCreate(BaseModel):
    name: str
    cuisine: str
    city: str


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    cuisine: Optional[str] = None
    city: Optional[str] = None


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    total_amount: float
    status: str = "PLACED"
    delivery_address: Optional[str] = None
    contact_phone: Optional[str] = None
    items: Optional[List[str]] = None
    special_instructions: Optional[str] = None
    payment_method: Optional[str] = None


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    restaurant_id: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    delivery_address: Optional[str] = None
    contact_phone: Optional[str] = None
    items: Optional[List[str]] = None
    special_instructions: Optional[str] = None
    payment_method: Optional[str] = None


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str
    status: str


class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    amount: Optional[float] = None
    method: Optional[str] = None
    status: Optional[str] = None


class DeliveryCreate(BaseModel):
    order_id: int
    rider_name: str
    current_location: str
    status: str


class DeliveryUpdate(BaseModel):
    order_id: Optional[int] = None
    rider_name: Optional[str] = None
    current_location: Optional[str] = None
    status: Optional[str] = None

SERVICES = {
    "user": "http://localhost:8021",
    "restaurant": "http://localhost:8022",
    "order": "http://localhost:8023",
    "payment": "http://localhost:8024",
    "delivery": "http://localhost:8025",
}


async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service '{service}' not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"HTTP method '{method}' not allowed")

            return JSONResponse(content=response.json() if response.text else None, status_code=response.status_code)
        except httpx.TimeoutException:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"Service '{service}' timed out")
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service '{service}' unavailable: {str(e)}")


@app.get("/")
def read_root():
    return {"message": "Food Delivery API Gateway is running", "available_services": list(SERVICES.keys())}


@app.get("/gateway/users/read-all")
async def get_all_users():
    return await forward_request("user", "/api/users/read-all", "GET")


@app.get("/gateway/users/read/{user_id}")
async def get_user(user_id: int):
    return await forward_request("user", f"/api/users/read/{user_id}", "GET")


@app.post("/gateway/users/create")
async def create_user(user: UserCreate):
    return await forward_request("user", "/api/users/create", "POST", json=user.model_dump())


@app.put("/gateway/users/update/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    return await forward_request("user", f"/api/users/update/{user_id}", "PUT", json=user.model_dump(exclude_none=True))


@app.delete("/gateway/users/delete/{user_id}")
async def delete_user(user_id: int):
    return await forward_request("user", f"/api/users/delete/{user_id}", "DELETE")


@app.get("/gateway/restaurants/read-all")
async def get_all_restaurants():
    return await forward_request("restaurant", "/api/restaurants/read-all", "GET")


@app.get("/gateway/restaurants/read/{restaurant_id}")
async def get_restaurant(restaurant_id: int):
    return await forward_request("restaurant", f"/api/restaurants/read/{restaurant_id}", "GET")


@app.post("/gateway/restaurants/create")
async def create_restaurant(restaurant: RestaurantCreate):
    return await forward_request("restaurant", "/api/restaurants/create", "POST", json=restaurant.model_dump())


@app.put("/gateway/restaurants/update/{restaurant_id}")
async def update_restaurant(restaurant_id: int, restaurant: RestaurantUpdate):
    return await forward_request("restaurant", f"/api/restaurants/update/{restaurant_id}", "PUT", json=restaurant.model_dump(exclude_none=True))


@app.delete("/gateway/restaurants/delete/{restaurant_id}")
async def delete_restaurant(restaurant_id: int):
    return await forward_request("restaurant", f"/api/restaurants/delete/{restaurant_id}", "DELETE")


@app.get("/gateway/orders/read-all")
async def get_all_orders():
    return await forward_request("order", "/api/orders/read-all", "GET")


@app.get("/gateway/orders/read/{order_id}")
async def get_order(order_id: int):
    return await forward_request("order", f"/api/orders/read/{order_id}", "GET")


@app.post("/gateway/orders/create")
async def create_order(order: OrderCreate):
    return await forward_request("order", "/api/orders/create", "POST", json=order.model_dump())


@app.put("/gateway/orders/update/{order_id}")
async def update_order(order_id: int, order: OrderUpdate):
    return await forward_request("order", f"/api/orders/update/{order_id}", "PUT", json=order.model_dump(exclude_none=True))


@app.delete("/gateway/orders/delete/{order_id}")
async def delete_order(order_id: int):
    return await forward_request("order", f"/api/orders/delete/{order_id}", "DELETE")


@app.get("/gateway/payments/read-all")
async def get_all_payments():
    return await forward_request("payment", "/api/payments/read-all", "GET")


@app.get("/gateway/payments/read/{payment_id}")
async def get_payment(payment_id: int):
    return await forward_request("payment", f"/api/payments/read/{payment_id}", "GET")


@app.post("/gateway/payments/create")
async def create_payment(payment: PaymentCreate):
    return await forward_request("payment", "/api/payments/create", "POST", json=payment.model_dump())


@app.put("/gateway/payments/update/{payment_id}")
async def update_payment(payment_id: int, payment: PaymentUpdate):
    return await forward_request("payment", f"/api/payments/update/{payment_id}", "PUT", json=payment.model_dump(exclude_none=True))


@app.delete("/gateway/payments/delete/{payment_id}")
async def delete_payment(payment_id: int):
    return await forward_request("payment", f"/api/payments/delete/{payment_id}", "DELETE")


@app.get("/gateway/deliveries/read-all")
async def get_all_deliveries():
    return await forward_request("delivery", "/api/deliveries/read-all", "GET")


@app.get("/gateway/deliveries/read/{delivery_id}")
async def get_delivery(delivery_id: int):
    return await forward_request("delivery", f"/api/deliveries/read/{delivery_id}", "GET")


@app.post("/gateway/deliveries/create")
async def create_delivery(delivery: DeliveryCreate):
    return await forward_request("delivery", "/api/deliveries/create", "POST", json=delivery.model_dump())


@app.put("/gateway/deliveries/update/{delivery_id}")
async def update_delivery(delivery_id: int, delivery: DeliveryUpdate):
    return await forward_request("delivery", f"/api/deliveries/update/{delivery_id}", "PUT", json=delivery.model_dump(exclude_none=True))


@app.delete("/gateway/deliveries/delete/{delivery_id}")
async def delete_delivery(delivery_id: int):
    return await forward_request("delivery", f"/api/deliveries/delete/{delivery_id}", "DELETE")
