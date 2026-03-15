from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ---------------------------------
# PRODUCT DATABASE
# ---------------------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

# ---------------------------------
# Pydantic Model
# ---------------------------------

class NewProduct(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str
    in_stock: bool = True


# ---------------------------------
# Helper function
# ---------------------------------

def find_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return None


# ---------------------------------
# GET ALL PRODUCTS
# ---------------------------------

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# ---------------------------------
# ADD PRODUCT (POST)
# ---------------------------------

@app.post("/products")
def add_product(data: NewProduct, response: Response):

    for p in products:
        if p["name"] == data.name:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product with this name already exists"}

    next_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": next_id,
        "name": data.name,
        "price": data.price,
        "category": data.category,
        "in_stock": data.in_stock
    }

    products.append(new_product)

    response.status_code = status.HTTP_201_CREATED

    return {
        "message": "Product added",
        "product": new_product
    }


# ---------------------------------
# PRODUCT AUDIT (Q5)
# ---------------------------------

@app.get("/products/audit")
def product_audit():

    in_stock_list = [p for p in products if p["in_stock"]]
    out_stock_list = [p for p in products if not p["in_stock"]]

    stock_value = sum(p["price"] * 10 for p in in_stock_list)

    priciest = max(products, key=lambda p: p["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p["name"] for p in out_stock_list],
        "total_stock_value": stock_value,
        "most_expensive": {
            "name": priciest["name"],
            "price": priciest["price"]
        }
    }


# ---------------------------------
# GET PRODUCT BY ID
# ---------------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    return product


# ---------------------------------
# UPDATE PRODUCT (PUT)
# ---------------------------------

@app.put("/products/{product_id}")
def update_product(
        product_id: int,
        price: Optional[int] = None,
        in_stock: Optional[bool] = None,
        response: Response = None
):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    if price is not None:
        product["price"] = price

    if in_stock is not None:
        product["in_stock"] = in_stock

    return {
        "message": "Product updated",
        "product": product
    }


# ---------------------------------
# DELETE PRODUCT
# ---------------------------------

@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)

    return {
        "message": f"Product '{product['name']}' deleted"
    }
