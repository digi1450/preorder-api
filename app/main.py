from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import engine, Base, SessionLocal
from . import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Preorder Food API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Preorder API is running"}


# ---------- Categories ----------
@app.post("/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, payload)


@app.get("/categories", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)


# ---------- Menu Items ----------
@app.post("/menu-items", response_model=schemas.MenuItemOut, status_code=201)
def create_menu_item(payload: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return crud.create_menu_item(db, payload)


@app.get("/menu-items", response_model=list[schemas.MenuItemOut])
def list_menu_items(db: Session = Depends(get_db)):
    return crud.list_menu_items(db)


@app.get("/menu-items/{item_id}", response_model=schemas.MenuItemOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@app.patch("/menu-items/{item_id}", response_model=schemas.MenuItemOut)
def update_menu_item(item_id: int, payload: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    item = crud.get_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return crud.update_menu_item(db, item, payload)


@app.delete("/menu-items/{item_id}", status_code=204)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    crud.delete_menu_item(db, item)
    return