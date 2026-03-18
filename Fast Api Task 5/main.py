from fastapi import FastAPI, Query, HTTPException
from typing import List, Dict, Optional
app = FastAPI(title="Smart Product & Order API")
PRODUCTS: List[Dict] = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

ORDERS: List[Dict] = []
order_counter = 1

def apply_search(data, keyword: Optional[str]):
    if keyword:
        return [item for item in data if keyword.lower() in item["name"].lower()]
    return data

def apply_sort(data, sort_by: str, order: str):
    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")

    return sorted(data, key=lambda x: x[sort_by], reverse=(order == "desc"))
def apply_pagination(data, page: int, limit: int):
    total = len(data)
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),
        "items": data[start:end]
    }
@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    result = apply_search(PRODUCTS, keyword)

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }

@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):
    sorted_data = apply_sort(PRODUCTS, sort_by, order)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_data
    }
@app.get("/products/page")
def paginate_products(
    page: int = Query(1, ge=1),
    limit: int = Query(2, ge=1)
):
    return apply_pagination(PRODUCTS, page, limit)

@app.get("/products/sort-by-category")
def sort_by_category():
    data = sorted(PRODUCTS, key=lambda x: (x["category"], x["price"]))

    return {
        "total": len(data),
        "products": data
    }
@app.get("/products/browse")
def browse_products(
    keyword: Optional[str] = None,
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1)
):
    result = PRODUCTS
    result = apply_search(result, keyword)
    result = apply_sort(result, sort_by, order)
    paginated = apply_pagination(result, page, limit)

    return {
        "filters": {
            "keyword": keyword,
            "sort_by": sort_by,
            "order": order
        },
        "total_found": len(result),
        **paginated
    }
@app.post("/orders")
def create_order(customer_name: str = Query(...)):
    global order_counter

    new_order = {
        "order_id": order_counter,
        "customer_name": customer_name
    }

    ORDERS.append(new_order)
    order_counter += 1

    return {"message": "Order created successfully", "order": new_order}
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = [
        o for o in ORDERS
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }
@app.get("/orders/page")
def paginate_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1)
):
    return apply_pagination(ORDERS, page, limit)