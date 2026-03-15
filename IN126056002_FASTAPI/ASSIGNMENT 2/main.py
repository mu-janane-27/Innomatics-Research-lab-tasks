from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# -------------------------------
# PRODUCT DATABASE
# -------------------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": True},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]

feedback = []


# ------------------------------------------------
# GET ALL PRODUCTS
# ------------------------------------------------

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# ------------------------------------------------
# FILTER PRODUCTS (DAY 2 TASK 1)
# ------------------------------------------------

@app.get("/products/filter")
def filter_products(
    category: Optional[str] = None,
    min_price: Optional[int] = Query(None, description="Minimum price"),
    max_price: Optional[int] = Query(None, description="Maximum price")
):

    result = products

    if category:
        result = [p for p in result if p["category"] == category]

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    return {
        "products": result,
        "total": len(result)
    }


# ------------------------------------------------
# GET PRODUCT PRICE ONLY (DAY 2 TASK 2)
# ------------------------------------------------

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error": "Product not found"}


# ------------------------------------------------
# CUSTOMER FEEDBACK MODEL (DAY 2 TASK 3)
# ------------------------------------------------

class CustomerFeedback(BaseModel):

    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


# ------------------------------------------------
# SUBMIT FEEDBACK
# ------------------------------------------------

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }


# ------------------------------------------------
# PRODUCT SUMMARY DASHBOARD (DAY 2 TASK 4)
# ------------------------------------------------

@app.get("/products/summary")
def product_summary():

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])

    categories = list(set(p["category"] for p in products))

    return {

        "total_products": len(products),

        "in_stock_count": len(in_stock),

        "out_of_stock_count": len(out_stock),

        "most_expensive": {
            "name": expensive["name"],
            "price": expensive["price"]
        },

        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },

        "categories": categories
    }


# ------------------------------------------------
# BULK ORDER MODEL (DAY 2 TASK 5)
# ------------------------------------------------

class BulkOrder(BaseModel):

    customer_name: str = Field(..., min_length=2)

    product_ids: list[int] = Field(..., min_items=1)


# ------------------------------------------------
# PLACE BULK ORDER
# ------------------------------------------------

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    ordered_products = []

    for pid in order.product_ids:

        product = next((p for p in products if p["id"] == pid), None)

        if not product:
            return {"error": f"Product {pid} not found"}

        if not product["in_stock"]:
            return {"error": f"{product['name']} is out of stock"}

        ordered_products.append(product)

    total_price = sum(p["price"] for p in ordered_products)

    return {

        "customer": order.customer_name,

        "products": ordered_products,

        "total_items": len(ordered_products),

        "total_price": total_price,

        "message": "Order placed successfully"
    }
