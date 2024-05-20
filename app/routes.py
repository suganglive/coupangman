# routes.py
from flask import Blueprint, render_template

from app import db
from app.models import Product  # Import the Product model

main = Blueprint("main", __name__)


@main.route("/")
def index():
    products = Product.query.all()  # Query all products from the database
    return render_template(
        "index.html", products=products
    )  # Pass the products to the template


@main.route("/product")
def product():
    return render_template("product.html")
