from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from fastapishop.database import SessionDep
from fastapishop.models import UsersOrm, OrderOrm, OrderItemOrm, ProductOrm, CategoryOrm
from fastapishop.schemas import ProductResponse
from fastapishop.schemas.orders import OrderResponse, OrderCreate, OrderStatusUpdate
from fastapishop.security import get_current_user, get_current_admin

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/")
async def get_my_orders(sess: SessionDep, user: UsersOrm = Depends(get_current_user)):
    query = (
        select(OrderOrm)
        .where(OrderOrm.user_id == user.id)
        .order_by(OrderOrm.created_at)
        .options(selectinload(OrderOrm.order_items).selectinload(OrderItemOrm.product).selectinload(ProductOrm.category))
    )

    result = await sess.execute(query)

    orders = result.scalars().all()

    orders_response = [OrderResponse.model_validate(order) for order in orders]

    return orders_response

@router.post("/")
async def create_order(order_data: OrderCreate, sess: SessionDep, user: UsersOrm = Depends(get_current_user)):
    product_ids = [order_item.product_id for order_item in order_data.order_items]
    requested_ids = set(product_ids)

    query = (
        select(ProductOrm)
        .where(ProductOrm.id.in_(product_ids))
    )

    result = await sess.execute(query)

    products = result.scalars().all()
    products_dict = {product.id: product for product in products}

    found_ids = {product.id for product in products}

    if requested_ids != found_ids:
        raise HTTPException(status_code=404, detail="Some products not found")

    new_order = OrderOrm(
        user_id=user.id
    )

    for order_item in order_data.order_items:
        product = products_dict[order_item.product_id]
        # if product.stock < order_item.quantity:
        #     raise HTTPException(status_code=409, detail="Stock less than quantity products in order")
        product.stock -= order_item.quantity

        new_order_item = OrderItemOrm(
            product=product,
            quantity=order_item.quantity,
            price=product.price
        )

        new_order.order_items.append(new_order_item)

    sess.add(new_order)
    await sess.commit()

    order_response = OrderResponse.model_validate(new_order)

    return order_response

@router.patch("/{order_id}/status")
async def update_order_status(order_id: int, order_data: OrderStatusUpdate, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(OrderOrm)
        .where(OrderOrm.id == order_id)
    )

    res = await sess.execute(query)

    order: OrderOrm = res.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail={"message": "Order not found"})

    order.status = order_data.status

    await sess.commit()

    return OrderResponse.model_validate(order)


@router.delete("/{order_id}")
async def delete_order(order_id: int, sess: SessionDep, user: UsersOrm = Depends(get_current_user)):
    query = (
        select(OrderOrm)
        .where(OrderOrm.id == order_id)
    )

    result = await sess.execute(query)

    order: OrderOrm = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail={"message":"Order not found"})

    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail={"message": "Forbidden"})

    await sess.delete(order)
    await sess.commit()

    return {"message":f"Order {order_id} deleted"}

@router.get("/{order_id}")
async def get_order(order_id: int, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(OrderOrm)
        .where(OrderOrm.id == order_id)
        .options(selectinload(OrderOrm.order_items).selectinload(OrderItemOrm.product))
    )

    res = await sess.execute(query)

    order = res.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail={"message":"Order not found"})

    return OrderResponse.model_validate(order)