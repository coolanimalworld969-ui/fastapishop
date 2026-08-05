from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import select, func

from database import SessionDep
from models import UsersOrm, OrderOrm, OrderStatus, OrderItemOrm
from security import get_current_admin

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
async def get_analytics(sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(
            func.count(func.distinct(OrderOrm.id)),
            func.sum(OrderItemOrm.price*OrderItemOrm.quantity)
        )
        .join(OrderOrm)
        .where(OrderOrm.status != OrderStatus.CANCELLED)
    )

    query2 = (
        select(
            OrderItemOrm.order_id,
            func.sum(
                OrderItemOrm.price*OrderItemOrm.quantity
            ).label("total_price")
        )
        .join(OrderOrm)
        .where(OrderOrm.status == OrderStatus.COMPLETED)
        .group_by(OrderItemOrm.order_id)
        .subquery()
    )

    query_avg = (
        select(
            func.avg(query2.c.total_price)
        )
    )

    query_users = (
        select(func.count(UsersOrm.id))
        .where(UsersOrm.is_active == True)
    )

    count_users = await sess.scalar(query_users)

    exec = await sess.execute(query)
    exec2 = await sess.execute(query_avg)

    total_orders, total_benefit = exec.one()
    if total_benefit is None:
        total_benefit = Decimal("0")
    avg_pay = exec2.scalar()
    avg_pay = round(avg_pay,1) if avg_pay is not None else 0

    response_data = {
        "total_orders" : total_orders,
        "total_benefit" : total_benefit,
        "avg_pay" : avg_pay,
        "total_users" : count_users
    }

    return response_data

