import re
from datetime import datetime, timedelta

import pandas as pd
from flask import Blueprint, render_template, request
from sqlalchemy import or_
from sqlalchemy.orm import aliased

from app import db  # Ensure this imports the same db instance
from app.models import (  # Import the Product model
    Feature,
    Product,
    ProductLowestPriceHistory,
)

# Aliases for the Feature table to handle different filter criteria
size_feature = aliased(Feature)
panel_feature = aliased(Feature)
resolution_feature = aliased(Feature)
release_year_feature = aliased(Feature)
smart_tv_feature = aliased(Feature)
game_mode_feature = aliased(Feature)

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


def get_release_years():
    # Query to get all features where the name matches the pattern "??년형" and sort them in descending order
    release_years = (
        Feature.query.filter(Feature.name.op("regexp")("^[0-9]{4}년형$"))
        .order_by(Feature.name.desc())
        .all()
    )

    # Extract the name values
    release_years_values = [feature.name for feature in release_years]

    # Filter out any empty values
    filtered_values = [
        release_year for release_year in release_years_values if release_year
    ]

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


def get_price_history(product_id):
    today = datetime.today().date()
    start_date = today - timedelta(days=89)

    price_history = (
        ProductLowestPriceHistory.query.filter(
            ProductLowestPriceHistory.product_id == product_id,
            ProductLowestPriceHistory.date >= start_date,
        )
        .order_by(ProductLowestPriceHistory.date)
        .all()
    )

    data = {
        "date": [record.date for record in price_history],
        "price": [record.lowest_price for record in price_history],
    }

    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)

    # Handle duplicate dates by aggregating prices, e.g., taking the average price
    df = df.groupby("date").agg({"price": "mean"})

    # Reindex to ensure 90 days coverage
    all_dates = pd.date_range(start=start_date, end=today)
    df = df.reindex(all_dates)

    # Fill missing values with the oldest day's price
    if not df.empty:
        # df.fillna(method="ffill", inplace=True)
        # df.fillna(
        #     method="bfill", inplace=True
        # )  # Just in case the first few days are missing
        df.ffill(inplace=True)
        df.bfill(inplace=True)
    else:
        df = pd.DataFrame(index=all_dates, columns=["price"]).fillna(
            0
        )  # Default to zero if no data

    return df


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

    selected_others_param = request.args.get("other", "")
    selected_others = selected_others_param.split("|") if selected_others_param else []
    print("Selected others: ", selected_others)

    selected_release_years_param = request.args.get("release_year", "")
    selected_release_years = (
        selected_release_years_param.split("|") if selected_release_years_param else []
    )
    print("Selected release years: ", selected_release_years)

    # # Filtering products based on selected brands
    # query = Product.query
    # Filtering products based on selected brands
    query = Product.query.filter(Product.best_offer.is_(True))

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

    # # Apply other filters (smart_tv and game_mode)
    # if "smart_tv" in selected_others or "game_mode" in selected_others:
    #     query = query.join(Feature, Product.features)

    #     other_conditions = []
    #     if "smart_tv" in selected_others:
    #         other_conditions.append(Feature.feature_code == 4)
    #     if "game_mode" in selected_others:
    #         other_conditions.append(Feature.name == "게임모드")

    #     query = query.filter(or_(*other_conditions))

    if "smart_tv" in selected_others:
        query = query.join(smart_tv_feature, Product.features).filter(
            smart_tv_feature.feature_code == 4,
        )

    if "game_mode" in selected_others:
        query = query.join(game_mode_feature, Product.features).filter(
            game_mode_feature.name == "게임모드",
        )

    if selected_release_years:
        query = query.join(release_year_feature, Product.features).filter(
            release_year_feature.name.in_(selected_release_years)
        )

    products = query.all()
    # for product in products:
    # print(f"Database - Lowest Price: {product.lowest_price}")

    features = db.session.query(Feature.name).distinct().all()
    features = [feature[0] for feature in features]
    sizes = get_screen_sizes()
    panels = get_display_techs()
    resolutions = get_resolutions()
    brands = db.session.query(Product.brand).distinct().all()
    brands = [brand[0] for brand in brands]  # Unpack tuples
    release_years = get_release_years()

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
        selected_others=selected_others,
        release_years=release_years,
        selected_release_years=selected_release_years,
    )


@main.route("/model/<int:id>", methods=["GET"])
def model(id):
    product = Product.query.get_or_404(id)
    features = get_product_features(id)
    df = get_price_history(id)
    data = {
        "dates": [(date - df.index[0]).days for date in df.index],
        "prices": df["price"].tolist(),
    }
    return render_template(
        "model.html",
        product=product,
        features=features,
        price_history=data,
    )