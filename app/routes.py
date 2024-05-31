# routes.py
import re

from flask import Blueprint, render_template, request

from app import db
from app.models import Feature, Product  # Import the Product model

main = Blueprint("main", __name__)


def find_matches(pattern, items):
    """
    Find all items in the list that match the given regex pattern.

    :param pattern: Regex pattern to match.
    :param items: List of strings to search.
    :return: List of matching items.
    """
    regex = re.compile(pattern)
    matches = [item for item in items if regex.search(item)]
    return matches


pattern_size = r"\d+인치\(\d+cm\)"
pattern_panel = r"ED$"
# Pattern to match strings that do not match pattern_size or pattern_panel
pattern_resol = r"^(?!.*\d+인치\(\d+cm\))(?!.*ED$)(?!^[가-힣]+$).*$"


@main.route("/", methods=["GET"])
def index():
    selected_brands_param = request.args.get("brand", "")
    selected_brands = selected_brands_param.split("|") if selected_brands_param else []
    print("Selected Brands:", selected_brands)  # Debugging print

    selected_sizes_param = request.args.get("size", "")
    selected_sizes = selected_sizes_param.split("|") if selected_sizes_param else []
    print("Selected Sizes: ", selected_sizes)

    selected_panels_param = request.args.get("panel", "")
    selected_panels = selected_panels_param.split("|") if selected_panels_param else []
    print("Selected Panels: ", selected_panels)

    selected_resolutions_param = request.args.get("resolution", "")
    selected_resolutions = (
        selected_resolutions_param.split("|") if selected_resolutions_param else []
    )
    print("Selected resolutions: ", selected_resolutions)

    # Filtering products based on selected brands
    query = Product.query

    if selected_brands:
        query = query.filter(Product.brand.in_(selected_brands))

    if selected_sizes:
        query = query.join(Product.features).filter(Feature.name.in_(selected_sizes))

    if selected_panels:
        query = query.join(Product.features).filter(Feature.name.in_(selected_panels))

    if selected_resolutions:
        query = query.join(Product.features).filter(
            Feature.name.in_(selected_resolutions)
        )

    products = query.all()

    features = db.session.query(Feature.name).distinct().all()
    features = [feature[0] for feature in features]
    sizes = find_matches(pattern_size, features)
    resolutions = find_matches(pattern_resol, features)
    panels = find_matches(pattern_panel, features)

    brands = db.session.query(Product.brand).distinct().all()
    brands = [brand[0] for brand in brands]  # Unpack tuples

    return render_template(
        "index.html",
        products=products,
        brands=brands,
        selected_brands=selected_brands,
        sizes=sizes,
        selected_sizes=selected_sizes,
        resolutions=resolutions,
        selected_resolutions=selected_resolutions,
        panels=panels,
        selected_panels=selected_panels,
    )


# @main.route("/")
# def index():
#     products = Product.query.all()  # Query all products from the database
#     return render_template(
#         "index.html", products=products
#     )  # Pass the products to the template


# @main.route("/?")
# def filter():
#     selected_brands = request.args.getlist("brand")
#     print(selected_brands)
#     # Filtering products based on selected brands
#     if selected_brands:
#         products = Product.query.filter(Product.brand.in_(selected_brands)).all()
#     else:
#         products = Product.query.all()
#     return render_template("index.html", products=products)


# @main.route("/product")
# def product():
#     return render_template("product.html")
