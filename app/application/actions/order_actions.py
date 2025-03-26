from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from app.domain.services.order_service import OrderService


class OrderAction(Action):
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def name(self) -> str:
        return "action_confirm_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        
        items = tracker.get_slot("items")
        user_id = tracker.sender_id

        try:
            order = self.order_service.create_order(items, user_id)
            dispatcher.utter_message(
                text=f"Order created! ID: {order.id}"
            )
        except Exception as e:
            dispatcher.utter_message(
                text="Error creating order. Please try again."
            )
            
