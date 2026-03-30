from models import Delivery


class DeliveryMockDataService:
    def __init__(self):
        self.deliveries = [
            Delivery(id=1, order_id=1, rider_name="Sanjeewa", current_location="Nugegoda", status="PICKED"),
            Delivery(id=2, order_id=2, rider_name="Malitha", current_location="Peradeniya", status="ASSIGNED"),
            Delivery(id=3, order_id=3, rider_name="Tharushi", current_location="Galle Fort", status="DELIVERED"),
        ]
        self.next_id = 4

    def get_all_deliveries(self):
        return self.deliveries

    def get_delivery_by_id(self, delivery_id: int):
        return next((d for d in self.deliveries if d.id == delivery_id), None)

    def add_delivery(self, delivery_data):
        new_delivery = Delivery(id=self.next_id, **delivery_data.model_dump())
        self.deliveries.append(new_delivery)
        self.next_id += 1
        return new_delivery

    def update_delivery(self, delivery_id: int, delivery_data):
        delivery = self.get_delivery_by_id(delivery_id)
        if delivery:
            update_data = delivery_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(delivery, key, value)
            return delivery
        return None

    def delete_delivery(self, delivery_id: int):
        delivery = self.get_delivery_by_id(delivery_id)
        if delivery:
            self.deliveries.remove(delivery)
            return True
        return False
