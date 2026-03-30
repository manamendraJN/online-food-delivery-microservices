from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
import httpx
from typing import Any

app = FastAPI(title="Food Delivery API Gateway", version="1.0.0")

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


@app.get("/gateway/users")
async def get_all_users():
    return await forward_request("user", "/api/users", "GET")


@app.get("/gateway/users/{user_id}")
async def get_user(user_id: int):
    return await forward_request("user", f"/api/users/{user_id}", "GET")


@app.post("/gateway/users")
async def create_user(request: Request):
    body = await request.json()
    return await forward_request("user", "/api/users", "POST", json=body)


@app.put("/gateway/users/{user_id}")
async def update_user(user_id: int, request: Request):
    body = await request.json()
    return await forward_request("user", f"/api/users/{user_id}", "PUT", json=body)


@app.delete("/gateway/users/{user_id}")
async def delete_user(user_id: int):
    return await forward_request("user", f"/api/users/{user_id}", "DELETE")


@app.get("/gateway/restaurants")
async def get_all_restaurants():
    return await forward_request("restaurant", "/api/restaurants", "GET")


@app.get("/gateway/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: int):
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "GET")


@app.post("/gateway/restaurants")
async def create_restaurant(request: Request):
    body = await request.json()
    return await forward_request("restaurant", "/api/restaurants", "POST", json=body)


@app.put("/gateway/restaurants/{restaurant_id}")
async def update_restaurant(restaurant_id: int, request: Request):
    body = await request.json()
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "PUT", json=body)


@app.delete("/gateway/restaurants/{restaurant_id}")
async def delete_restaurant(restaurant_id: int):
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "DELETE")


@app.get("/gateway/orders")
async def get_all_orders():
    return await forward_request("order", "/api/orders", "GET")


@app.get("/gateway/orders/{order_id}")
async def get_order(order_id: int):
    return await forward_request("order", f"/api/orders/{order_id}", "GET")


@app.post("/gateway/orders")
async def create_order(request: Request):
    body = await request.json()
    return await forward_request("order", "/api/orders", "POST", json=body)


@app.put("/gateway/orders/{order_id}")
async def update_order(order_id: int, request: Request):
    body = await request.json()
    return await forward_request("order", f"/api/orders/{order_id}", "PUT", json=body)


@app.delete("/gateway/orders/{order_id}")
async def delete_order(order_id: int):
    return await forward_request("order", f"/api/orders/{order_id}", "DELETE")


@app.get("/gateway/payments")
async def get_all_payments():
    return await forward_request("payment", "/api/payments", "GET")


@app.get("/gateway/payments/{payment_id}")
async def get_payment(payment_id: int):
    return await forward_request("payment", f"/api/payments/{payment_id}", "GET")


@app.post("/gateway/payments")
async def create_payment(request: Request):
    body = await request.json()
    return await forward_request("payment", "/api/payments", "POST", json=body)


@app.put("/gateway/payments/{payment_id}")
async def update_payment(payment_id: int, request: Request):
    body = await request.json()
    return await forward_request("payment", f"/api/payments/{payment_id}", "PUT", json=body)


@app.delete("/gateway/payments/{payment_id}")
async def delete_payment(payment_id: int):
    return await forward_request("payment", f"/api/payments/{payment_id}", "DELETE")


@app.get("/gateway/deliveries")
async def get_all_deliveries():
    return await forward_request("delivery", "/api/deliveries", "GET")


@app.get("/gateway/deliveries/{delivery_id}")
async def get_delivery(delivery_id: int):
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "GET")


@app.post("/gateway/deliveries")
async def create_delivery(request: Request):
    body = await request.json()
    return await forward_request("delivery", "/api/deliveries", "POST", json=body)


@app.put("/gateway/deliveries/{delivery_id}")
async def update_delivery(delivery_id: int, request: Request):
    body = await request.json()
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "PUT", json=body)


@app.delete("/gateway/deliveries/{delivery_id}")
async def delete_delivery(delivery_id: int):
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "DELETE")
