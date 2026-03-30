from models import Order


class OrderMockDataService:
    def __init__(self):
        self.orders = [
            Order(id=1, user_id=1, restaurant_id=1, total_amount=2450.0, status="PLACED"),
            Order(id=2, user_id=2, restaurant_id=2, total_amount=3200.0, status="PREPARING"),
            Order(id=3, user_id=3, restaurant_id=3, total_amount=1800.0, status="DELIVERED"),
        ]
        self.next_id = 4

    def get_all_orders(self):
        return self.orders

    def get_order_by_id(self, order_id: int):
        return next((o for o in self.orders if o.id == order_id), None)

    def add_order(self, order_data):
        new_order = Order(id=self.next_id, **order_data.model_dump())
        self.orders.append(new_order)
        self.next_id += 1
        return new_order

    def update_order(self, order_id: int, order_data):
        order = self.get_order_by_id(order_id)
        if order:
            update_data = order_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(order, key, value)
            return order
        return None

    def delete_order(self, order_id: int):
        order = self.get_order_by_id(order_id)
        if order:
            self.orders.remove(order)
            return True
        return False
