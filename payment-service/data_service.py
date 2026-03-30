from models import Payment


class PaymentMockDataService:
    def __init__(self):
        self.payments = [
            Payment(id=1, order_id=1, amount=2450.0, method="CARD", status="PAID"),
            Payment(id=2, order_id=2, amount=3200.0, method="CASH", status="PENDING"),
            Payment(id=3, order_id=3, amount=1800.0, method="CARD", status="PAID"),
        ]
        self.next_id = 4

    def get_all_payments(self):
        return self.payments

    def get_payment_by_id(self, payment_id: int):
        return next((p for p in self.payments if p.id == payment_id), None)

    def add_payment(self, payment_data):
        new_payment = Payment(id=self.next_id, **payment_data.model_dump())
        self.payments.append(new_payment)
        self.next_id += 1
        return new_payment

    def update_payment(self, payment_id: int, payment_data):
        payment = self.get_payment_by_id(payment_id)
        if payment:
            update_data = payment_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(payment, key, value)
            return payment
        return None

    def delete_payment(self, payment_id: int):
        payment = self.get_payment_by_id(payment_id)
        if payment:
            self.payments.remove(payment)
            return True
        return False
