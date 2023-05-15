from enum import Enum
from typing import List, ForwardRef

from pydantic import BaseModel, Field, validator

from utils import check_time_format


class CourierType(str, Enum):
    auto = "AUTO"
    bike = "BIKE"
    foot = "FOOT"


class CreateCourierDto(BaseModel):
    courier_type: CourierType = Field(description="Тип курьера",
                                      nullable=False,
                                      example="AUTO")
    regions: List[int] = Field(description="Регионы которые обслуживает курьер",
                               default=[1, 2, 3],
                               nullable=False,
                               example=[1, 2, 3])

    working_hours: List[str] = Field(description="Время работы курьера",
                                     default=["12:00-15:00"],
                                     nullable=False,
                                     example=["12:00-15:00"])

    _validate_hours = validator('working_hours', allow_reuse=True, each_item=True, always=True)(check_time_format)

    class Config:
        orm_mode = True


class CourierDto(BaseModel):
    courier_id: int = Field(description="Идентификатор курьера")
    courier_type: CourierType
    regions: List[int] = Field()
    working_hours: List[str] = Field(default=["12:00-15:00"])

    _validate_hours = validator('working_hours', allow_reuse=True, each_item=True, always=True)(check_time_format)

    class Config:
        orm_mode = True


class CreateCourierRequest(BaseModel):
    couriers: List[ForwardRef('CreateCourierDto')]


class GetCouriersResponse(BaseModel):
    couriers: List[ForwardRef('CourierDto')]
    limit: int
    offset: int


class GetCourierMetaInfoResponse(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: List[int] = Field()
    working_hours: List[str] = Field()
    rating: int
    earnings: int

    _validate_hours = validator('working_hours', allow_reuse=True, each_item=True, always=True)(check_time_format)
