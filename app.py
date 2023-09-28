from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    inspect,
    create_engine,
    insert,
    select,
    text,
    func,
    ForeignKey,
    Float,
    DateTime,
    Identity,
)

import uuid

import os

from sqlalchemy.exc import IntegrityError
from utils import get_engine, run_query
from flask import Flask, request, render_template

# from image import image_bp
from home import home_bp
# from auth import signup_bp, signin_bp
# from product_list import product_bp, category_bp
# from product_detail import details_bp, cart_bp
# from cart import address_bp, shipping_bp, order_bp
# from profil_page import user_bp
# from admin_page import get_orders_bp, create_product_bp, update_product_bp, delete_product_bp, create_category_bp, update_category_bp, delete_category_bp, get_sales_bp

from flask_cors import CORS

if os.path.exists('scrapingdb.db'):
   os.remove('scrapingdb.db')

def create_app():
    app = Flask(__name__,template_folder='./templates',static_folder='./static')

    CORS(app)

    @app.route('/home')
    def index():
        return render_template('index.html')

    engine = get_engine()

    # if not inspect(engine).has_table("users"):
    #     meta = MetaData()
    #     Table(
    #         "users",
    #         meta,
    #         Column("id", Integer, primary_key=True),
    #         Column("name", String, nullable=False),
    #         Column("email", String, nullable=False),
    #         Column("password", String, nullable=False),
    #         Column("phone_number", String, nullable=False),
    #         Column("type", String, nullable=False),
    #         Column("token", String),
    #         Column("balance", Integer, nullable=False, server_default="0"),
    #         Column("reguler", Integer, nullable=False, server_default="0"),
    #         Column("next_day", Integer, nullable=False, server_default="0"),
    #         Column("created_at", DateTime, nullable=False, server_default=func.now()),
    #         Column("update_at", DateTime),
    #         Column("deleted_at", DateTime),
    #     )
    #     meta.create_all(engine)

    # #Insert Admin into Table
    # run_query(f"INSERT INTO users(name,email,password,phone_number,type) VALUES('Admin','admin@gmail.com','Admin123','085253545556','seller') ON CONFLICT DO NOTHING", commit=True)
    # #Insert Admin into Table

    # if not inspect(engine).has_table("address"):
    #     meta = MetaData()
    #     Table(
    #         "address",
    #         meta,
    #         Column("id", Integer, primary_key=True),
    #         Column("email", String),
    #         Column("name", String),
    #         Column("phone_number", String),
    #         Column("address", String),
    #         Column("city", String)
    #     )
    #     meta.create_all(engine)

    # #Insert Address into Table
    # run_query(f"INSERT INTO address VALUES(1,'blackcity@gmail.com','Kantor','085212345678','Jln. in aja dulu, lama lama juga nyaman','Jaksel') ON CONFLICT DO NOTHING", commit=True)
    # #Insert Address into Table

    # if not inspect(engine).has_table("cart"):
    #     meta = MetaData()
    #     Table(
    #         "cart",
    #         meta,
    #         Column("email", String),
    #         Column("id", String),
    #         Column("size", String),
    #         Column("price", Integer),
    #         Column("amount", Integer),
    #     )
    #     meta.create_all(engine)

    # if not inspect(engine).has_table("orders"):
    #     meta = MetaData()
    #     Table(
    #         "orders",
    #         meta,
    #         Column("id", String),
    #         Column("email", String),
    #         Column("product_id", String),
    #         Column("size", String),
    #         Column("price", Integer),
    #         Column("amount", Integer),
    #         Column("name_add", String),
    #         Column("phone_number", String),
    #         Column("address", String),
    #         Column("city", String),
    #         Column("shipping_method", String),
    #         Column("created_at", DateTime)
    #     )
    #     meta.create_all(engine)

    # if not inspect(engine).has_table("banner"):
    #     meta = MetaData()    
    #     Table(
    #         "banner",
    #         meta,
    #         Column("id", String, nullable=False),
    #         Column("image", String, nullable=False),
    #         Column("title", String, primary_key=True)
    #     )
    #     meta.create_all(engine)

    # #Insert Banner into Table
    # banner1 = uuid.uuid4()
    # run_query(f"INSERT INTO banner VALUES('{banner1}','/images/banner/Banner1.jpeg','Banner Cover') ON CONFLICT DO NOTHING", commit=True)
    
    # banner2 = uuid.uuid4()
    # run_query(f"INSERT INTO banner VALUES('{banner2}','/images/banner/Banner2.jpeg','Banner Significant Event') ON CONFLICT DO NOTHING", commit=True)
    # #Insert Banner into Table

    # if not inspect(engine).has_table("categories"):
    #     meta = MetaData()    
    #     Table(
    #         "categories",
    #         meta,
    #         Column("id", Integer),
    #         Column("image", String),
    #         Column("title", String, primary_key=True),
    #         Column("created_at", DateTime, nullable=False, server_default=func.now()),
    #         Column("update_at", DateTime),
    #         Column("deleted_at", DateTime),
    #     )
    #     meta.create_all(engine)

    # #Insert Categories into Table
    # # category1 = uuid.uuid4()
    # run_query(f"INSERT INTO categories VALUES(1,'/images/categories/top.jpeg','TOP',current_timestamp,NULL,NULL) ON CONFLICT DO NOTHING", commit=True)
    # # category2 = uuid.uuid4()
    # run_query(f"INSERT INTO categories VALUES(2,'/images/categories/bottom.jpeg','BOTTOM',current_timestamp,NULL,NULL) ON CONFLICT DO NOTHING", commit=True)
    # # category3 = uuid.uuid4()
    # run_query(f"INSERT INTO categories VALUES(3,'/images/categories/footwear.jpeg','FOOTWEAR',current_timestamp,NULL,NULL) ON CONFLICT DO NOTHING", commit=True)
    # # category4 = uuid.uuid4()
    # run_query(f"INSERT INTO categories VALUES(4,'/images/categories/accessories.jpeg','ACCESSORIES',current_timestamp,NULL,NULL) ON CONFLICT DO NOTHING", commit=True)
    # run_query(f"INSERT INTO categories VALUES(5,'/images/categories/sets.jpg','SETS',current_timestamp,current_timestamp,current_timestamp) ON CONFLICT DO NOTHING", commit=True)
    # #Insert Categories into Table

    if not inspect(engine).has_table("product"):
        meta = MetaData()    
        Table(
            "product",
            meta,
            Column("id", Integer, primary_key=True),
            Column("source", String),
            Column("image", String, nullable=False),
            Column("title", String, nullable=False),
            Column("price", Integer, server_default="0"),
            Column("sold", Integer, server_default="0"),
            Column("location", String, nullable=False),
            Column("link", String, nullable=False),
        )
        meta.create_all(engine) 

    # if not inspect(engine).has_table("pages"):
    #     meta = MetaData()    
    #     Table(
    #         "pages",
    #         meta,
    #         Column("keyword", String),
    #         Column("page", String),
    #     )
    #     meta.create_all(engine)

    
    # # run_query(f"INSERT INTO pages VALUES('','0') ON CONFLICT DO NOTHING;", commit=True)

    # #Insert Product into Table
    # product1 = uuid.uuid4()
    # run_query(f"INSERT INTO product VALUES('{product1}','gambar1','Kids Tshirt Cartoon Baby Bus',80000,2,'Kota Depok','link1') ON CONFLICT DO NOTHING", commit=True)
    # product2 = uuid.uuid4()
    # run_query(f"INSERT INTO product VALUES('{product2}','gambar2','Vans Black n White',80000,92,'Kota Bekasi','link2') ON CONFLICT DO NOTHING", commit=True)
    # product3 = uuid.uuid4()
    # run_query(f"INSERT INTO product VALUES('{product3}','gambar3','Jeans Denim Man Black',250000,45,'Jakarta Utara','link3') ON CONFLICT DO NOTHING", commit=True)
    # product4 = uuid.uuid4()
    # run_query(f"INSERT INTO product VALUES('{product4}','gambar4','Rolex Watch Ruby For Men',250000,39,'Makassar','link4') ON CONFLICT DO NOTHING", commit=True)
    # #Insert Product into Table

    blueprints = [home_bp]

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


app = create_app()
app.run()
