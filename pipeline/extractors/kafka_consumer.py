import json
import os
from kafka import KafkaConsumer


class OrderEventConsumer:
    def __init__(self, topic: str, group_id: str):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=os.getenv("KAFKA_BROKERS", "localhost:9092"),
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    def stream(self):
        for message in self.consumer:
            yield message.value
