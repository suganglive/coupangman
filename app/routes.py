import re

from flask import Blueprint, render_template, request
from sqlalchemy.orm import aliased

from app import db
from app.models import Feature, Product  # Import the Product model

# Aliases for the Feature table to handle different filter criteria
size_feature = aliased(Feature)
panel_feature = aliased(Feature)
resolution_feature = aliased(Feature)

main = Blueprint("main", __name__)


def get_screen_sizes():
    # Query to get all feature values where name is 'screen_size'
    screen_sizes = Feature.query.filter_by(name="screen_size").all()
    screen_size_values = [feature.value for feature in screen_sizes]

    # Filter out entries containing 'cm' and empty strings
    filtered_screen_sizes = [
        size for size in screen_size_values if size and "cm" not in size
    ]

    # Sort the filtered screen sizes
    def parse_size(size):
        try:
            return int(size.replace("인치", ""))
        except ValueError:
            return float("inf")  # handle non-integer sizes gracefully

    sorted_screen_sizes = sorted(filtered_screen_sizes, key=parse_size)

    return sorted_screen_sizes


def get_display_techs():
    display_techs = Feature.query.filter_by(name="display_tech").all()
    display_tech_values = [feature.value for feature in display_techs]

    filtered_values = [
        display_tech for display_tech in display_tech_values if display_tech
    ]
    return filtered_values


def get_resolutions():
    resolutions = Feature.query.filter_by(name="resolution").all()
    resolution_values = [feature.value for feature in resolutions]

    filtered_values = [resolution for resolution in resolution_values if resolution]

    return filtered_values


def get_product_features(product_id):
    product = Product.query.get(product_id)
    features = product.features

    # Organize features by feature_code
    feature_dict = {}
    for feature in features:
        if feature.feature_code not in feature_dict:
            feature_dict[feature.feature_code] = []
        feature_dict[feature.feature_code].append(feature)

    return feature_dict


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
        query = query.join(size_feature, Product.features).filter(
            size_feature.value.in_(selected_sizes)
        )

    if selected_panels:
        query = query.join(panel_feature, Product.features).filter(
            panel_feature.value.in_(selected_panels)
        )

    if selected_resolutions:
        query = query.join(resolution_feature, Product.features).filter(
            resolution_feature.value.in_(selected_resolutions)
        )

    products = query.all()

    features = db.session.query(Feature.name).distinct().all()
    features = [feature[0] for feature in features]
    sizes = get_screen_sizes()
    panels = get_display_techs()
    resolutions = get_resolutions()
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


@main.route("/model/<int:id>", methods=["GET"])
def model(id):
    product = Product.query.get_or_404(id)
    features = get_product_features(id)
    return render_template("model.html", product=product, features=features)
