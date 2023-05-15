import datetime
from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi.responses import JSONResponse

from database import get_async_session
from orders.schemas import CreateOrderRequest, OrderDto, CompleteOrderRequestDto
from orders.models import order, courier_order
from courier_controller.models import courier
from ratelimit import limiter

router = APIRouter(
    prefix="/orders",
    tags=["order-controller"]
)


@router.get("", response_model=List[OrderDto])
@limiter.limit("10/second")
async def getOrders(request: Request, limit: int = 1, offset: int = 0,
                    session: AsyncSession = Depends(get_async_session)):
    j = order.join(courier_order, courier_order.c.order_id == order.c.order_id, isouter=True)
    query = select(order, courier_order.c.complete_time).select_from(j).order_by(order.c.order_id).limit(limit).offset(offset)
    result = await session.execute(query)
    orders = [dict(i) for i in result.mappings()]
    for o in orders:
        if o['complete_time'] is not None:
            o['complete_time'] = datetime.datetime.isoformat(o['complete_time'])[:-3] + "Z"
    return orders


@router.get("/{order_id}", response_model=OrderDto)
@limiter.limit("10/second")
async def getOrderById(request: Request, order_id: int, session: AsyncSession = Depends(get_async_session)):
    j = order.join(courier_order, courier_order.c.order_id == order.c.order_id, isouter=True)
    query = select(order, courier_order.c.complete_time).select_from(j).where(order.c.order_id == order_id)
    result = dict(*(await session.execute(query)).mappings())
    if result:
        if result['complete_time'] is not None:
            result['complete_time'] = datetime.datetime.isoformat(result['complete_time'])[:-3] + "Z"
        return result
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=jsonable_encoder({'detail': f'order {order_id} not found'}))


@router.post("", response_model=CreateOrderRequest)
@limiter.limit("10/second")
async def createOrder(request: Request, new_orders: CreateOrderRequest,
                      session: AsyncSession = Depends(get_async_session)):
    for c in new_orders.orders:
        stmt = insert(order).values(c.dict())
        await session.execute(stmt)
        await session.commit()
    return new_orders


@router.post("/complete", response_model=List[OrderDto])
@limiter.limit("10/second")
async def completeOrder(request: Request, order_info: CompleteOrderRequestDto,
                        session: AsyncSession = Depends(get_async_session)):
    added_orders = []
    added_couriers = []
    orders_in_db = set((await session.execute(select(order.c.order_id).select_from(order))).scalars())
    courier_in_db = set((await session.execute(select(courier.c.courier_id).select_from(courier))).scalars())
    completed_orders = set(
        (await session.execute(select(courier_order.c.order_id).select_from(courier_order))).scalars())
    for info in order_info.complete_info:
        if info.order_id not in orders_in_db:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={'detail': f'order {info.order_id} does not exist'})
        if info.courier_id not in courier_in_db:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={'detail': f'courier {info.courier_id} does not exist'})
        if info.order_id in completed_orders:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={'detail': f'order {info.order_id} is already completed'})
        added_orders.append(info.order_id)
        added_couriers.append(info.courier_id)
        stmt = insert(courier_order).values(info.dict())
        await session.execute(stmt)
        await session.commit()
    j = courier_order.join(order,
                           order.c.order_id == courier_order.c.order_id).join(courier,
                                                                              courier.c.courier_id == courier_order.c.courier_id)
    query = select(order, courier_order.c.complete_time).select_from(j).filter(order.c.order_id.in_(added_orders))
    result = await session.execute(query)
    orders = [dict(i) for i in result.mappings()]
    for o in orders:
        o['complete_time'] = datetime.datetime.isoformat(o['complete_time'])[:-3]+"Z"
    return orders
