import pika
import json
import os
from .entities import Insumo

class ServicioValidacionStock:
    @staticmethod
    def validar(insumo: Insumo, cantidad: int) -> bool:
        return insumo.verificar_disponibilidad(cantidad)

class ServicioAjusteStock:
    @staticmethod
    def ajustar(insumo: Insumo, cantidad: int) -> None:
        insumo.descontar_stock(cantidad)

class EventPublisher:
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

    def publish(self, event):
        connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        channel = connection.channel()
        channel.exchange_declare(exchange='events', exchange_type='topic')
        channel.basic_publish(exchange='events', routing_key='inventario.event', body=json.dumps(event.__dict__))
        connection.close()