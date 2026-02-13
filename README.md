# Preorder Food API

## Overview
This project is a **RESTful API for a food preorder system** built using:

- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

The system allows customers to **preorder food with a selected pickup time**,  
and the server will automatically calculate:

- Food preparation start time (`send_time`)
- Order total price
- Order status management

---

## Features

### Category Management
- Create category
- List categories

### Menu Item Management
- Create menu item
- List menu items
- Get menu item by ID
- Update menu item
- Delete menu item

### Order Management
- Create order with multiple items
- Automatically calculate:
  - `send_time`
  - `total_amount`
- List all orders
- Filter orders by status
- Get order by ID
- Update pickup time or status
- Cancel order

---

## Project Structure

```
preorder-api/
├── app/
│   ├── main.py        # FastAPI entry point
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic schemas
│   ├── crud.py        # Database logic
│   └── db.py          # Database connection
├── requirements.txt
└── README.md
```

---

## Installation & Run

```bash
# 1) Clone repository
git clone https://github.com/digi1450/preorder-api.git
cd preorder-api

# 2) Create virtual environment
python3 -m venv venv

# 3) Activate virtual environment (macOS / Linux)
source venv/bin/activate

# 4) Install dependencies
pip install -r requirements.txt

# 5) Run FastAPI server
uvicorn app.main:app --reload
```

Open Swagger documentation in browser:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Categories
```
POST   /categories        Create category
GET    /categories        List categories
```

### Menu Items
```
POST   /menu-items              Create menu item
GET    /menu-items              List menu items
GET    /menu-items/{item_id}    Get menu item
PATCH  /menu-items/{item_id}    Update menu item
DELETE /menu-items/{item_id}    Delete menu item
```

### Orders
```
POST   /orders                    Create order
GET    /orders                    List orders (optional ?status= filter)
GET    /orders/{order_id}         Get order by ID
PATCH  /orders/{order_id}         Update pickup time or status
POST   /orders/{order_id}/cancel  Cancel order
```

---

## Example: Create Order Request

```json
{
  "customer_name": "Digi",
  "phone": "0912345678",
  "pickup_time": "2026-02-13T18:30:00",
  "items": [
    {
      "item_id": 1,
      "quantity": 2
    }
  ]
}
```

---

## Testing

You can test the API using:

- **Swagger UI** → `/docs`
- **Postman**
- **curl**

All CRUD operations should return proper HTTP status codes such as:

- `201 Created`
- `200 OK`
- `400 Bad Request`
- `404 Not Found`

---

## Author

**Digi**  
Computer Science Student