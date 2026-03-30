from data_service import OrderMockDataService


class OrderService:
    def __init__(self):
        self.data_service = OrderMockDataService()

    def get_all(self):
        return self.data_service.get_all_orders()

    def get_by_id(self, order_id: int):
        return self.data_service.get_order_by_id(order_id)

    def create(self, order_data):
        return self.data_service.add_order(order_data)

    def update(self, order_id: int, order_data):
        return self.data_service.update_order(order_id, order_data)

    def delete(self, order_id: int):
        return self.data_service.delete_order(order_id)
