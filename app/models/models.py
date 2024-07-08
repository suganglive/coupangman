from datetime import date

from flask_sqlalchemy import SQLAlchemy

from app import db

# db = SQLAlchemy()

# Association table for many-to-many relationship between Product and Feature
product_features = db.Table(
    "product_features",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column("feature_id", db.Integer, db.ForeignKey("feature.id"), primary_key=True),
)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(255), nullable=False)
    model_name = db.Column(db.String(255), nullable=False)
    install_info = db.Column(db.String(50), nullable=False)
    tv_type = db.Column(db.String(50), nullable=False)
    product_pic_s = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.String(50), nullable=False)
    rating_count = db.Column(db.String(50), nullable=False)
    original_price = db.Column(db.Float, nullable=True)
    sale_price = db.Column(db.Float, nullable=True)
    coupon_price = db.Column(db.Float, nullable=True)
    highest_price = db.Column(db.Float, nullable=True)
    lowest_price = db.Column(db.Float, nullable=True)
    discount_rate = db.Column(db.Float, nullable=True)
    brand = db.Column(db.String(50), nullable=False)
    product_url = db.Column(db.String(255), nullable=False)
    shorten_url = db.Column(db.String(255), nullable=True)
    last_checked = db.Column(db.Date, nullable=False, default=date.today)
    features_scraped = db.Column(db.Boolean, nullable=False, default=False)
    best_offer = db.Column(db.Boolean, nullable=False, default=False)

    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint(
            "name", "model_name", "tv_type", name="_name_model_tvtype_uc"
        ),
    )

    # Relationship with Feature
    features = db.relationship(
        "Feature",
        secondary=product_features,
        backref=db.backref("products", lazy=True),
    )
    # Relationship with ProductLowestPriceHistory
    lowest_price_history = db.relationship(
        "ProductLowestPriceHistory", backref="product", lazy=True
    )


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature_code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)


class ProductLowestPriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    lowest_price = db.Column(db.Float, nullable=False)

    # Relationship to Product is already established in Product class
