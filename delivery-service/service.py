from data_service import DeliveryMockDataService


class DeliveryService:
    def __init__(self):
        self.data_service = DeliveryMockDataService()

    def get_all(self):
        return self.data_service.get_all_deliveries()

    def get_by_id(self, delivery_id: int):
        return self.data_service.get_delivery_by_id(delivery_id)

    def create(self, delivery_data):
        return self.data_service.add_delivery(delivery_data)

    def update(self, delivery_id: int, delivery_data):
        return self.data_service.update_delivery(delivery_id, delivery_data)

    def delete(self, delivery_id: int):
        return self.data_service.delete_delivery(delivery_id)
