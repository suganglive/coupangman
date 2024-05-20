from .. import db


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
    original_price = db.Column(db.String(50), nullable=False)
    sale_price = db.Column(db.String(50), nullable=False)
    coupon_price = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    product_url = db.Column(db.String(255), nullable=False)
