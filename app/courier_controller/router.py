from datetime import date

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import insert, text, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from courier_controller.models import courier
from orders.models import courier_order, order
from courier_controller.schemas import CreateCourierRequest, CourierDto, GetCouriersResponse, GetCourierMetaInfoResponse
from ratelimit import limiter

router = APIRouter(
    prefix="/couriers",
    tags=["courier-controller"]
)


@router.get("/assigments")
def couriersAssignments(date: str, courier_id: int):
    return {"test"}


@router.get(
    "",
    response_model=GetCouriersResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("10/second")
async def getCouriers(request: Request, limit: int = 1, offset: int = 0,
                      session: AsyncSession = Depends(get_async_session)):
    query = select(courier).limit(limit).offset(offset)
    result = await session.execute(query)
    couriers = [dict(i) for i in result.mappings()]
    return {"couriers": couriers, "limit": limit, "offset": offset}


@router.get("/{courier_id}", response_model=CourierDto)
@limiter.limit("10/second")
async def getCourierById(request: Request, courier_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(courier).where(courier.c.courier_id == courier_id)
    result = dict(*(await session.execute(query)).mappings())
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'detail': f'courier {courier_id} not found'})


@router.post("", response_model=CreateCourierRequest)
@limiter.limit("10/second")
async def createCourier(request: Request, new_couriers: CreateCourierRequest,
                        session: AsyncSession = Depends(get_async_session)):
    for c in new_couriers.couriers:
        stmt = insert(courier).values(c.dict())
        await session.execute(stmt)
        await session.commit()
    return new_couriers


@router.get("/meta-info/{courier_id}", response_model=GetCourierMetaInfoResponse)
@limiter.limit("10/second")
async def getCourierMetaInfo(request: Request, courier_id: int, startDate: date, endDate: date,
                             session: AsyncSession = Depends(get_async_session)):
    courier_in_db = set((await session.execute(select(courier.c.courier_id).select_from(courier))).scalars())
    if courier_id not in courier_in_db:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'detail': f'courier {courier_id} does not exist'})
    datediff = (endDate - startDate).days * 24
    subq_courier = select(courier).where(courier.c.courier_id == courier_id).subquery()
    courier_type = await session.scalar(select(subq_courier.c.courier_type).select_from(subq_courier))
    if courier_type == "FOOT":
        earn_c, rate_c = 2, 3
    elif courier_type == "BIKE":
        earn_c, rate_c = 3, 2
    elif courier_type == "AUTO":
        earn_c, rate_c = 4, 1
    j = courier_order.join(subq_courier, courier_order.c.courier_id == subq_courier.c.courier_id).join(order,
                                                                                                       order.c.order_id == courier_order.c.order_id)
    query = select((func.count(order.c.cost) / datediff * rate_c).label("rating"),
                   (func.sum(order.c.cost) * earn_c).label("earnings")).select_from(j).where(
        courier_order.c.complete_time >= startDate).where(courier_order.c.complete_time < endDate)
    result = await session.execute(query)
    result = [i for i in result.mappings()]
    res = await getCourierById(request, courier_id, session)
    res.update(result[0])
    res["rating"] = round(res["rating"])
    return res
