import pika
import json
import os
from .entities import Entrega

class ServicioEntrega:
    @staticmethod
    def procesar_entrega(entrega: Entrega):
        # Logic to process entrega
        pass

class EventPublisher:
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

    def publish(self, event):
        connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        channel = connection.channel()
        channel.exchange_declare(exchange='events', exchange_type='topic')
        channel.basic_publish(exchange='events', routing_key='distribucion.event', body=json.dumps(event.__dict__))
        connection.close()