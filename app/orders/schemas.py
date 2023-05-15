import datetime
from typing import List, ForwardRef, Optional

from pydantic import BaseModel, Field, validator

from utils import check_time_format, check_datetime_format


class CreateOrderDto(BaseModel):
    weight: float = Field(ge=0)
    regions: int = Field()
    delivery_hours: List[str] = Field(default=["11:00-20:00"])
    cost: int

    _validate_hours = validator('delivery_hours', allow_reuse=True, each_item=True, always=True)(check_time_format)

    class Config:
        orm_mode = True


class OrderDto(BaseModel):
    order_id: int
    weight: float = Field(description='Вес заказа', ge=0)
    regions: int = Field()
    delivery_hours: List[str] = Field()
    cost: int = Field(description='Стоимость заказа')
    complete_time: Optional[str] = None

    _validate_hours = validator('delivery_hours', allow_reuse=True, each_item=True, always=True)(check_time_format)


    class Config:
        orm_mode = True


class CreateOrderRequest(BaseModel):
    orders: List[ForwardRef('CreateOrderDto')]


class CompleteOrder(BaseModel):
    courier_id: int
    order_id: int
    complete_time: str = Field(description="Время выполнения заказа",
                               default=datetime.datetime.utcnow().isoformat()[:-3] + "Z")

    _validate_complete_time = validator('complete_time', allow_reuse=True, always=True)(check_datetime_format)

    class Config:
        orm_mode = True


class CompleteOrderRequestDto(BaseModel):
    complete_info: List[ForwardRef('CompleteOrder')]
