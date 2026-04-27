import os
from sqlalchemy import create_engine, text


class WarehouseLoader:
    def __init__(self):
        self.engine = create_engine(
            os.getenv("WAREHOUSE_URL", "postgresql://localhost:5432/warehouse")
        )

    def load_order(self, order: dict):
        with self.engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO orders_fact (order_id, user_id, total_cents, item_count, processed_at)
                    VALUES (:id, :userId, :total_cents, :item_count, :processed_at)
                    ON CONFLICT (order_id) DO UPDATE SET total_cents = :total_cents
                """),
                order,
            )
