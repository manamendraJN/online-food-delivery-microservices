from models import Restaurant


class RestaurantMockDataService:
    def __init__(self):
        self.restaurants = [
            Restaurant(id=1, name="Spice House", cuisine="Sri Lankan", city="Colombo"),
            Restaurant(id=2, name="Pizza Point", cuisine="Italian", city="Kandy"),
            Restaurant(id=3, name="Tokyo Bowl", cuisine="Japanese", city="Galle"),
        ]
        self.next_id = 4

    def get_all_restaurants(self):
        return self.restaurants

    def get_restaurant_by_id(self, restaurant_id: int):
        return next((r for r in self.restaurants if r.id == restaurant_id), None)

    def add_restaurant(self, restaurant_data):
        new_restaurant = Restaurant(id=self.next_id, **restaurant_data.model_dump())
        self.restaurants.append(new_restaurant)
        self.next_id += 1
        return new_restaurant

    def update_restaurant(self, restaurant_id: int, restaurant_data):
        restaurant = self.get_restaurant_by_id(restaurant_id)
        if restaurant:
            update_data = restaurant_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(restaurant, key, value)
            return restaurant
        return None

    def delete_restaurant(self, restaurant_id: int):
        restaurant = self.get_restaurant_by_id(restaurant_id)
        if restaurant:
            self.restaurants.remove(restaurant)
            return True
        return False
