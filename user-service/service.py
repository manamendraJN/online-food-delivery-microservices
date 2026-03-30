from data_service import UserMockDataService


class UserService:
    def __init__(self):
        self.data_service = UserMockDataService()

    def get_all(self):
        return self.data_service.get_all_users()

    def get_by_id(self, user_id: int):
        return self.data_service.get_user_by_id(user_id)

    def create(self, user_data):
        return self.data_service.add_user(user_data)

    def update(self, user_id: int, user_data):
        return self.data_service.update_user(user_id, user_data)

    def delete(self, user_id: int):
        return self.data_service.delete_user(user_id)
