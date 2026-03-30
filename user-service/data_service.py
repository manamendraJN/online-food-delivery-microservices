from models import User


class UserMockDataService:
    def __init__(self):
        self.users = [
            User(id=1, name="Kamal Perera", email="kamal@example.com", phone="0771000001"),
            User(id=2, name="Nadeesha Silva", email="nadeesha@example.com", phone="0771000002"),
            User(id=3, name="Ravi Fernando", email="ravi@example.com", phone="0771000003"),
        ]
        self.next_id = 4

    def get_all_users(self):
        return self.users

    def get_user_by_id(self, user_id: int):
        return next((u for u in self.users if u.id == user_id), None)

    def add_user(self, user_data):
        new_user = User(id=self.next_id, **user_data.model_dump())
        self.users.append(new_user)
        self.next_id += 1
        return new_user

    def update_user(self, user_id: int, user_data):
        user = self.get_user_by_id(user_id)
        if user:
            update_data = user_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)
            return user
        return None

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            return True
        return False
