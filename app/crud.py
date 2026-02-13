from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta


# -------- Categories --------
def create_category(db: Session, payload: schemas.CategoryCreate) -> models.Category:
    c = models.Category(name=payload.name)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def list_categories(db: Session) -> list[models.Category]:
    return db.query(models.Category).order_by(models.Category.id.asc()).all()


# -------- Menu Items --------
def create_menu_item(db: Session, payload: schemas.MenuItemCreate) -> models.MenuItem:
    item = models.MenuItem(
        name=payload.name,
        price=payload.price,
        category_id=payload.category_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_menu_items(db: Session) -> list[models.MenuItem]:
    return db.query(models.MenuItem).order_by(models.MenuItem.id.asc()).all()


def get_menu_item(db: Session, item_id: int) -> models.MenuItem | None:
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()


def update_menu_item(db: Session, item: models.MenuItem, payload: schemas.MenuItemUpdate) -> models.MenuItem:
    if payload.name is not None:
        item.name = payload.name
    if payload.price is not None:
        item.price = payload.price
    if payload.category_id is not None:
        item.category_id = payload.category_id

    db.commit()
    db.refresh(item)
    return item


def delete_menu_item(db: Session, item: models.MenuItem) -> None:
    db.delete(item)
    db.commit()

PREP_MINUTES_DEFAULT = 20
ALLOWED_STATUSES = {"pending", "preparing", "ready", "picked_up", "cancelled"}


def create_order(db: Session, payload: schemas.OrderCreate) -> models.Order:
    # 1) validate pickup_time
    now = datetime.utcnow()
    prep_minutes = PREP_MINUTES_DEFAULT
    min_pickup = now + timedelta(minutes=prep_minutes)

    if payload.pickup_time < min_pickup:
        raise ValueError(f"pickup_time must be at least {prep_minutes} minutes from now")

    # 2) calculate send_time
    send_time = payload.pickup_time - timedelta(minutes=prep_minutes)

    # 3) create order
    order = models.Order(
        customer_name=payload.customer_name,
        phone=payload.phone,
        pickup_time=payload.pickup_time,
        send_time=send_time,
        prep_minutes=prep_minutes,
        status="pending",
        total_amount=0,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # 4) create order items + compute total
    total = 0.0
    for it in payload.items:
        menu_item = get_menu_item(db, it.item_id)
        if not menu_item:
            raise ValueError(f"menu item {it.item_id} not found")

        unit_price = float(menu_item.price)
        subtotal = unit_price * it.quantity
        total += subtotal

        oi = models.OrderItem(
            order_id=order.id,
            item_id=it.item_id,
            quantity=it.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )
        db.add(oi)

    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session, status: str | None = None) -> list[models.Order]:
    q = db.query(models.Order).order_by(models.Order.id.desc())
    if status:
        q = q.filter(models.Order.status == status)
    return q.all()


def get_order(db: Session, order_id: int) -> models.Order | None:
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order(db: Session, order: models.Order, payload: schemas.OrderUpdate) -> models.Order:
    changed = False

    if payload.pickup_time is not None:
        # validate + recalc send_time
        now = datetime.utcnow()
        min_pickup = now + timedelta(minutes=order.prep_minutes)
        if payload.pickup_time < min_pickup:
            raise ValueError(f"pickup_time must be at least {order.prep_minutes} minutes from now")

        order.pickup_time = payload.pickup_time
        order.send_time = payload.pickup_time - timedelta(minutes=order.prep_minutes)
        changed = True

    if payload.status is not None:
        if payload.status not in ALLOWED_STATUSES:
            raise ValueError("invalid status")
        order.status = payload.status
        changed = True

    if changed:
        db.commit()
        db.refresh(order)

    return order


def cancel_order(db: Session, order: models.Order) -> models.Order:
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return order