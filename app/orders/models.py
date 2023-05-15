from datetime import datetime

from sqlalchemy import Integer, Table, Column, JSON, Float, TIMESTAMP, ForeignKey, MetaData

metadata = MetaData()

from courier_controller.models import courier
order = Table(
    "orders",
    metadata,
    Column("order_id", Integer, primary_key=True, autoincrement=True),
    Column("weight", Float, nullable=False),
    Column("regions", Integer, nullable=False),
    Column("delivery_hours", JSON, nullable=False),
    Column("cost", Integer, nullable=False)
)

courier_order = Table(
    "courier_order",
    metadata,
    Column("courier_id", Integer, ForeignKey(courier.c.courier_id)),
    Column("order_id", Integer, ForeignKey(order.c.order_id)),
    Column("complete_time", TIMESTAMP, default=datetime.utcnow)
)
