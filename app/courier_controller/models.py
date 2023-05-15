from sqlalchemy import Integer, Table, Column, JSON, String, MetaData

metadata = MetaData()

courier = Table(
    "courier",
    metadata,
    Column("courier_id", Integer, primary_key=True, autoincrement=True),
    Column("courier_type", String, nullable=False),
    Column("regions", JSON, nullable=False),
    Column("working_hours", JSON, nullable=False)
)
