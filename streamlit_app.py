# streamlit_app.py
import pandas as pd
import streamlit as st

from app import create_app, db
from app.models import Product

app = create_app()


@st.cache
def load_data():
    with app.app_context():
        products = Product.query.all()
        data = [
            {
                "Name": product.name,
                "Short Name": product.short_name,
                "Model Name": product.model_name,
                "Install Info": product.install_info,
                "TV Type": product.tv_type,
                "Product Pic": product.product_pic_s,
                "Rating": product.rating,
                "Review Count": product.count,
                "Original Price": product.original_price,
                "Sale Price": product.sale_price,
                "Coupon Price": product.coupon_price,
                "Brand": product.brand,
                "Product URL": product.product_url,
            }
            for product in products
        ]
        return pd.DataFrame(data)


st.title("Product List")
data = load_data()
st.dataframe(data)
