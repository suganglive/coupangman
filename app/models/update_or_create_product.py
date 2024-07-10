from datetime import date

from sqlalchemy.exc import IntegrityError

from app.models.models import Product, ProductLowestPriceHistory, db


def update_or_create_product(data):
    model_name = data["model_name"]
    tv_type = data["tv_type"]
    lowest_price = data["lowest_price"]
    name = data["name"]

    # Check if product exists
    product = Product.query.filter_by(
        name=name,
        model_name=model_name,
        tv_type=tv_type,
    ).first()

    if product:
        # Update existing product
        if product.last_checked != date.today():
            product.short_name = data["short_name"]
            product.install_info = data["install_info"]
            product.product_pic_s = data["product_pic_s"]
            product.rating = data["rating"]
            product.rating_count = data["rating_count"]
            product.original_price = data["original_price"]
            product.sale_price = data["sale_price"]
            product.coupon_price = data["coupon_price"]
            product.highest_price = data["highest_price"]
            product.lowest_price = data["lowest_price"]
            product.discount_rate = data["discount_rate"]
            product.brand = data["brand"]
            product.product_url = data["product_url"]
            product.last_checked = date.today()

            # Log the price history
            price_history = ProductLowestPriceHistory(
                product_id=product.id, date=date.today(), lowest_price=lowest_price
            )
            db.session.add(price_history)

        product.last_checked = date.today()
        db.session.commit()
    else:
        # Create a new product
        try:
            new_product = Product(
                name=data["name"],
                short_name=data["short_name"],
                model_name=model_name,
                install_info=data["install_info"],
                tv_type=tv_type,
                product_pic_s=data["product_pic_s"],
                rating=data["rating"],
                rating_count=data["rating_count"],
                original_price=data["original_price"],
                sale_price=data["sale_price"],
                coupon_price=data["coupon_price"],
                highest_price=data["highest_price"],
                lowest_price=lowest_price,
                discount_rate=data["discount_rate"],
                brand=data["brand"],
                product_url=data["product_url"],
                # shorten_url=data.get("shorten_url"),
                last_checked=date.today(),  # Set last_checked to today
            )
            db.session.add(new_product)
            db.session.commit()

            # Log the price history for the new product
            price_history = ProductLowestPriceHistory(
                product_id=new_product.id, date=date.today(), lowest_price=lowest_price
            )
            db.session.add(price_history)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Handle integrity error, maybe log it or raise an exception


def delete_old_products():
    today = date.today()
    # Delete products that were not checked today
    Product.query.filter(Product.last_checked != today).delete()
    Product.query.filter(Product.features_scraped == 0).delete()
    db.session.commit()


from sqlalchemy.sql import func

# from yourapp import db
# from yourapp.models import Product


def isit_best_offer():
    # Step 2: Query to find all unique (model_name, tv_type) combinations
    product_groups = (
        db.session.query(Product.model_name, Product.tv_type).distinct().all()
    )

    for group in product_groups:
        model_name, tv_type = group

        # Step 3: Find the product with the lowest price in each group
        lowest_priced_product = (
            db.session.query(Product)
            .filter_by(model_name=model_name, tv_type=tv_type)
            .order_by(Product.lowest_price)
            .first()
        )

        # Step 4: Set best_offer to True for the lowest priced product
        if lowest_priced_product:
            lowest_priced_product.best_offer = True

            # Set best_offer to False for other products in the group
            other_products = (
                db.session.query(Product)
                .filter(
                    Product.id != lowest_priced_product.id,
                    Product.model_name == model_name,
                    Product.tv_type == tv_type,
                )
                .all()
            )

            for product in other_products:
                product.best_offer = False

    # Commit the changes to the database
    db.session.commit()
