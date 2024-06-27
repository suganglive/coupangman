from custom_types import JSONEncodedDict

from .. import db

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
    count = db.Column(db.String(50), nullable=False)
    original_price = db.Column(db.String(50), nullable=True)
    sale_price = db.Column(db.String(50), nullable=True)
    coupon_price = db.Column(db.String(50), nullable=True)
    highest_price = db.Column(db.String(50), nullable=True)
    lowest_price = db.Column(db.String(50), nullable=True)
    discount_rate = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(50), nullable=False)
    product_url = db.Column(db.String(255), nullable=False)
    release = db.Column(db.String(50), nullable=False)
    shorten_url = db.Column(db.String(255), nullable=True)
    # Relationship with Feature
    features = db.relationship(
        "Feature",
        secondary=product_features,
        backref=db.backref("products", lazy="dynamic"),
    )


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature_code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
