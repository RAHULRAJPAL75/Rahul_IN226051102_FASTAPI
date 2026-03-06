# FastAPI Assignment 1

This assignment focuses on building REST API endpoints using **FastAPI**.  
All tasks should be implemented inside a single file named **main.py**.

---

## 1. Add Three New Products

### Scenario
The store has recently added three new products:
- Laptop Stand
- Mechanical Keyboard
- Webcam

These items need to be visible in the mobile application.

### Tasks
- Create the endpoint: **GET /products**
- Add **3 new products** to the `products` list in `main.py` with IDs **5, 6, and 7**

Each product must include the following fields:

- `id`
- `name`
- `price`
- `category`
- `in_stock`

---

## 2. Create a Category Filter Endpoint

### Scenario
The mobile application needs to display products based on their **category**.  
For example, one page should show **Electronics**, while another should show **Stationery** products.

### Tasks
- Create a new endpoint: **GET /products/category/{category_name}**
- Return only the products that match the given category
- If no products are found, return:

```json
{"error": "No products found in this category"}
````

---

## 3. Show Only In-Stock Products

### Scenario

Customers should not see products that are currently **out of stock**.
An endpoint is needed to return only the products that are available.

### Tasks

* Create endpoint: **GET /products/instock**
* Return only products where `in_stock = True`
* Also return the **total count of in-stock products**

---

## 4. Create a Store Summary Endpoint

### Scenario

The home screen of the mobile app needs a **quick overview of the store**.

### Tasks

Create endpoint: **GET /store/summary**

Return the following information:

* Total number of products
* Number of in-stock products
* Number of out-of-stock products
* A list of **unique categories** available in the store

---

## 5. Search Products by Name

### Scenario

Users should be able to search for products using a keyword in the search bar.

### Tasks

Create endpoint: **GET /products/search/{keyword}**

Requirements:

* Search must be **case-insensitive**
* Return products whose **name contains the keyword**
* Return the **total number of matches**

If no products match the search, return:

```json
{"message": "No products matched your search"}
```

---

## 6. Cheapest and Most Expensive Product

### Scenario

The application wants to highlight special products on the home screen.

* **Best Deal** → the product with the **lowest price**
* **Premium Pick** → the product with the **highest price**

### Tasks

Create endpoint: **GET /products/deals**

Return:

* `best_deal` → product with the lowest price
* `premium_pick` → product with the highest price

```


