from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="E-commerce FastAPI Project")

@app.get("/")
def welcome():
    return {
        "message": "Welcome to my Store API",
        "docs": "Visit /docs to test all endpoints"
    }

store_products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "USB Cable", "price": 199, "category": "Electronics", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

feedback_list = []
order_records = []
order_id_seq = 1


def find_product(pid: int):
    return next((item for item in store_products if item["id"] == pid), None)

def available_products():
    return list(filter(lambda x: x["in_stock"], store_products))

@app.get("/products")
def show_products():
    return {"total_items": len(store_products), "data": store_products}

@app.get("/products/category/{cat}")
def products_by_category(cat: str):
    matched = list(filter(lambda p: p["category"].lower() == cat.lower(), store_products))
    return {"category": cat, "count": len(matched), "items": matched}

@app.get("/products/available")
def show_available():
    items = available_products()
    return {"available_count": len(items), "items": items}

@app.get("/products/deals")
def product_deals():
    sorted_products = sorted(store_products, key=lambda x: x["price"])
    return {
        "cheapest_product": sorted_products[0],
        "most_expensive_product": sorted_products[-1]
    }

@app.get("/products/search")
def search_item(keyword: str):
    found = [p for p in store_products if keyword.lower() in p["name"].lower()]
    return {"search_keyword": keyword, "matches": found, "count": len(found)}

@app.get("/store/stats")
def store_stats():
    stock = available_products()
    out_stock = [p for p in store_products if not p["in_stock"]]

    category_set = {p["category"] for p in store_products}

    return {
        "store": "Online Shop",
        "product_count": len(store_products),
        "in_stock": len(stock),
        "out_of_stock": len(out_stock),
        "categories": list(category_set)
    }

@app.get("/products/filter")
def advanced_filter(
        category: Optional[str] = None,
        min_price: Optional[int] = Query(None),
        max_price: Optional[int] = Query(None)
):

    filtered = store_products.copy()

    if category:
        filtered = [p for p in filtered if p["category"].lower() == category.lower()]

    if min_price is not None:
        filtered = [p for p in filtered if p["price"] >= min_price]

    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]

    return {"filtered_products": filtered, "count": len(filtered)}

@app.get("/products/{pid}/price")
def product_price(pid: int):
    product = find_product(pid)

    if product:
        return {"product": product["name"], "price": product["price"]}

    return {"message": "Product not found"}

@app.get("/products/overview")
def overview():
    prices = [p["price"] for p in store_products]

    cheapest_price = min(prices)
    highest_price = max(prices)

    cheapest = next(p for p in store_products if p["price"] == cheapest_price)
    expensive = next(p for p in store_products if p["price"] == highest_price)

    return {
        "total_products": len(store_products),
        "in_stock_products": len(available_products()),
        "most_expensive": expensive,
        "cheapest": cheapest
    }

class Feedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

@app.post("/feedback")
def add_feedback(data: Feedback):
    record = data.dict()
    feedback_list.append(record)

    return {
        "status": "Feedback recorded",
        "total_feedback": len(feedback_list),
        "data": record
    }

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class BulkOrder(BaseModel):
    company_name: str
    contact_email: str
    items: List[OrderItem]

@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):

    successful = []
    rejected = []
    total_cost = 0

    for item in order.items:

        product = find_product(item.product_id)

        if not product:
            rejected.append({"product_id": item.product_id, "reason": "Invalid product"})
            continue

        if not product["in_stock"]:
            rejected.append({"product": product["name"], "reason": "Out of stock"})
            continue

        cost = product["price"] * item.quantity
        total_cost += cost

        successful.append({
            "product": product["name"],
            "quantity": item.quantity,
            "cost": cost
        })

    return {
        "company": order.company_name,
        "processed": successful,
        "failed": rejected,
        "total_bill": total_cost
    }
class OrderRequest(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders")
def place_order(order: OrderRequest):
    global order_id_seq

    order_data = {
        "order_id": order_id_seq,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending"
    }

    order_records.append(order_data)
    order_id_seq += 1

    return order_data

@app.get("/orders/{oid}")
def order_status(oid: int):

    order = next((o for o in order_records if o["order_id"] == oid), None)

    if order:
        return order

    return {"message": "Order not found"}

@app.patch("/orders/{oid}/confirm")
def confirm(oid: int):

    order = next((o for o in order_records if o["order_id"] == oid), None)

    if order:
        order["status"] = "confirmed"
        return {"message": "Order confirmed", "order": order}

    return {"message": "Order not found"}