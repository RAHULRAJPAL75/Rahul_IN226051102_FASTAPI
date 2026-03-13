from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="Store Product API")

inventory = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

def locate_product(pid: int):
    for item in inventory:
        if item["id"] == pid:
            return item
    return None

@app.get("/")
def welcome():
    return {"message": "Welcome to the Store API"}


@app.get("/products")
def list_products():
    return {
        "products": inventory,
        "total": len(inventory)
    }


@app.get("/products/{product_id}")
def product_detail(product_id: int, response: Response):

    item = locate_product(product_id)

    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    return item

@app.get("/products/category/{category_name}")
def products_by_category(category_name: str):

    filtered = [p for p in inventory if p["category"].lower() == category_name.lower()]

    if not filtered:
        return {"message": "No products available in this category"}

    return {
        "category": category_name,
        "items": filtered,
        "count": len(filtered)
    }


@app.get("/products/instock")
def available_products():

    stock_items = [p for p in inventory if p["in_stock"]]

    return {
        "available_products": stock_items,
        "count": len(stock_items)
    }


@app.get("/products/search/{keyword}")
def search_item(keyword: str):

    matches = [p for p in inventory if keyword.lower() in p["name"].lower()]

    if not matches:
        return {"message": "No matching products found"}

    return {
        "search_keyword": keyword,
        "results": matches,
        "matches": len(matches)
    }

@app.get("/products/filter")
def filter_products(
        min_price: Optional[int] = Query(None),
        max_price: Optional[int] = Query(None),
        category: Optional[str] = Query(None)
):

    results = inventory

    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]

    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]

    if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]

    return {
        "products": results,
        "total": len(results)
    }

class Feedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


reviews = []


@app.post("/feedback")
def add_feedback(data: Feedback):

    reviews.append(data.model_dump())

    return {
        "message": "Feedback recorded successfully",
        "feedback": data.model_dump(),
        "total_feedback": len(reviews)
    }

class ProductCreate(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool = True


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, response: Response):

    for p in inventory:
        if p["name"].lower() == product.name.lower():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product already exists"}

    new_id = max(p["id"] for p in inventory) + 1

    new_item = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    inventory.append(new_item)

    return {
        "message": "Product added successfully",
        "product": new_item
    }

@app.put("/products/{product_id}")
def modify_product(
        product_id: int,
        price: Optional[int] = Query(None),
        in_stock: Optional[bool] = Query(None),
        response: Response = None
):

    item = locate_product(product_id)

    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    if price is not None:
        item["price"] = price

    if in_stock is not None:
        item["in_stock"] = in_stock

    return {
        "message": "Product updated successfully",
        "product": item
    }

@app.delete("/products/{product_id}")
def remove_product(product_id: int, response: Response):

    item = locate_product(product_id)

    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    inventory.remove(item)

    return {
        "message": f"Product '{item['name']}' removed from store"
    }
@app.get("/products/audit")
def inventory_audit():

    available = [p for p in inventory if p["in_stock"]]
    unavailable = [p for p in inventory if not p["in_stock"]]

    total_value = sum(p["price"] * 10 for p in available)

    highest = max(inventory, key=lambda x: x["price"])

    return {
        "total_products": len(inventory),
        "in_stock_count": len(available),
        "out_of_stock_names": [p["name"] for p in unavailable],
        "total_stock_value": total_value,
        "most_expensive": {
            "name": highest["name"],
            "price": highest["price"]
        }
    }

@app.put("/products/discount")
def apply_category_discount(
        category: str = Query(...),
        discount_percent: int = Query(..., ge=1, le=99)
):

    modified = []

    for item in inventory:
        if item["category"].lower() == category.lower():

            new_price = int(item["price"] * (1 - discount_percent / 100))
            item["price"] = new_price

            modified.append({
                "name": item["name"],
                "new_price": new_price
            })

    if not modified:
        return {"message": "No products found for this category"}

    return {
        "updated_products": len(modified),
        "products": modified
    }