from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from app.domain.services.order_service import OrderService

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop
from rasa_sdk.types import DomainDict


MENU = {
    "ceviche": 35,
    "lomo saltado": 40,
    "pulpo a la parrilla": 45,
    "pizza calamar": 50,
    "tarta de maracuyá": 20,
    "ensalada capresa": 25
}


class ValidatePedidoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pedido_form"

    async def validate_item_comida(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        item = slot_value.lower()
        normalized_item = self.normalizar_item(item)

        if normalized_item in MENU:
            return {"item_comida": normalized_item}

        dispatcher.utter_message(
            text=f"Lo siento, no tenemos {item} en nuestro menú.")
        return {"item_comida": None}

    async def validate_cantidad(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            cantidad = int(slot_value)
            if cantidad > 0:
                return {"cantidad": cantidad}
        except:
            pass

        dispatcher.utter_message(
            text="Por favor ingresa una cantidad válida (ej. 1, 2, 3...)")
        return {"cantidad": None}

    def normalizar_item(self, item: Text) -> Text:
        correcciones = {
            "piza": "pizza calamar",
            "cebiche": "ceviche",
            "lasagña": "lasaña",
            "maracuya": "maracuyá"
        }
        return correcciones.get(item, item)


class ActionProveerPrecio(Action):
    def name(self) -> Text:
        return "action_proveer_precio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        item = tracker.get_slot("item_comida")
        precio = MENU.get(item, None)

        if precio:
            dispatcher.utter_message(
                response="utter_precio",
                item_comida=item.capitalize(),
                precio=f"S/ {precio}"
            )
        else:
            dispatcher.utter_message(
                text=f"Disculpa, no tenemos {item} en nuestro menú actual.")

        return []


class ActionManejarErrores(Action):
    def name(self) -> Text:
        return "action_manejar_errores"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="Lo siento, no entendí completamente. ¿Podrías reformular tu pregunta?")
        dispatcher.utter_message(response="utter_menu")

        return []


class ActionConfirmarPedido(Action):
    def name(self) -> Text:
        return "action_confirmar_pedido"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pedido_actual = tracker.get_slot("pedido_actual") or []
        item = tracker.get_slot("item_comida")
        cantidad = tracker.get_slot("cantidad")

        pedido_actual.append({
            "item": item,
            "cantidad": cantidad,
            "precio": MENU[item] * cantidad
        })

        total = sum(item["precio"] for item in pedido_actual)

        dispatcher.utter_message(
            response="utter_confirmacion_pedido",
            cantidad=cantidad,
            item_comida=item
        )

        return [
            SlotSet("pedido_actual", pedido_actual),
            SlotSet("item_comida", None),
            SlotSet("cantidad", None),
            ActiveLoop(None)
        ]


class ActionFinalizarPedido(Action):
    def name(self) -> Text:
        return "action_finalizar_pedido"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pedido = tracker.get_slot("pedido_actual") or []
        total = sum(item["precio"] for item in pedido)

        pedido_texto = "\n".join(
            [f"- {item['cantidad']x {item['item']} (S/ {item['precio']})"
             for item in pedido]
        )

        dispatcher.utter_message(
            response="utter_pedido_finalizado",
            pedido=pedido_texto,
            total=total
        )

        return [SlotSet("pedido_actual", None)]


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
