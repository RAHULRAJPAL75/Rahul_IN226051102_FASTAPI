from fastapi import FastAPI

app = FastAPI()


products = [
    {"id": 1, "name": "Smartphone", "price": 19999, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Bluetooth Speaker", "price": 2999, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Running Shoes", "price": 3999, "category": "Fashion", "in_stock": True},
    {"id": 4, "name": "Backpack", "price": 1499, "category": "Accessories", "in_stock": True},

    
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

@app.get("/")
def home():
    return {"message": "FastAPI Is Working"}

@app.get("/products")
def get_products():

    return {
        "products": products,
        "total": len(products)
    }

@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):

    products_by_category = [p for p in products if p["category"].lower() == category_name.lower()]

    if not products_by_category:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": products_by_category,
        "total": len(products_by_category)
    }

@app.get("/products/instock")
def get_instock_products():

    instock_products = [p for p in products if p["in_stock"]]

    return {
        "in_stock_products": instock_products,
        "count": len(instock_products)
    }

@app.get("/store/summary")
def store_summary():

    in_stock = len([p for p in products if p["in_stock"]])

    out_of_stock = len([p for p in products if not p["in_stock"]])

    
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }

@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    
    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "matched_products": matched_products,
        "total_matches": len(matched_products)
    }

 
@app.get("/products/deals")
def product_deals():

  
    best_deal = min(products, key=lambda p: p["price"])

    premium_pick = max(products, key=lambda p: p["price"])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }