from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Restaurant, RestaurantCreate, RestaurantUpdate
from service import RestaurantService

app = FastAPI(title="Restaurant Microservice", version="1.0.0")
restaurant_service = RestaurantService()


@app.get("/")
def read_root():
    return {"message": "Restaurant Microservice is running"}


@app.get("/api/restaurants", response_model=List[Restaurant])
def get_all_restaurants():
    try:
        return restaurant_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve restaurants: {str(e)}")


@app.get("/api/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: int):
    try:
        restaurant = restaurant_service.get_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with ID {restaurant_id} not found")
        return restaurant
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve restaurant: {str(e)}")


@app.post("/api/restaurants", response_model=Restaurant, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant: RestaurantCreate):
    try:
        return restaurant_service.create(restaurant)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create restaurant: {str(e)}")


@app.put("/api/restaurants/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: int, restaurant: RestaurantUpdate):
    try:
        updated_restaurant = restaurant_service.update(restaurant_id, restaurant)
        if not updated_restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with ID {restaurant_id} not found")
        return updated_restaurant
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update restaurant: {str(e)}")


@app.delete("/api/restaurants/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int):
    try:
        success = restaurant_service.delete(restaurant_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with ID {restaurant_id} not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete restaurant: {str(e)}")
