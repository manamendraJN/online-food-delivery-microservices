from fastapi import FastAPI, HTTPException, status
from typing import List
from models import User, UserCreate, UserUpdate
from service import UserService

app = FastAPI(title="User Microservice", version="1.0.0")
user_service = UserService()


@app.get("/")
def read_root():
    return {"message": "User Microservice is running"}


@app.get("/api/users/read-all", response_model=List[User])
def get_all_users():
    try:
        return user_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve users: {str(e)}")


@app.get("/api/users/read/{user_id}", response_model=User)
def get_user(user_id: int):
    try:
        user = user_service.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve user: {str(e)}")


@app.post("/api/users/create", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        return user_service.create(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create user: {str(e)}")


@app.put("/api/users/update/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate):
    try:
        updated_user = user_service.update(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update user: {str(e)}")


@app.delete("/api/users/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    try:
        success = user_service.delete(user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete user: {str(e)}")
