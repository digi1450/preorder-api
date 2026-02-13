from sqlalchemy.orm import Session
from . import models, schemas


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