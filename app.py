from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    inspect,
)

import uuid

import os

from sqlalchemy.exc import IntegrityError
from utils import get_engine, run_query
from flask import Flask, request, render_template

from home import home_bp

from flask_cors import CORS

if os.path.exists('scrapingdb.db'):
   os.remove('scrapingdb.db')

def create_app():
    app = Flask(__name__,template_folder='./templates',static_folder='./static')

    CORS(app)

    engine = get_engine()

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

    blueprints = [home_bp]

    for bp in blueprints:
        app.register_blueprint(bp)

    return app

app = create_app()
app.run()