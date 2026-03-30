from data_service import RestaurantMockDataService


class RestaurantService:
    def __init__(self):
        self.data_service = RestaurantMockDataService()

    def get_all(self):
        return self.data_service.get_all_restaurants()

    def get_by_id(self, restaurant_id: int):
        return self.data_service.get_restaurant_by_id(restaurant_id)

    def create(self, restaurant_data):
        return self.data_service.add_restaurant(restaurant_data)

    def update(self, restaurant_id: int, restaurant_data):
        return self.data_service.update_restaurant(restaurant_id, restaurant_data)

    def delete(self, restaurant_id: int):
        return self.data_service.delete_restaurant(restaurant_id)
