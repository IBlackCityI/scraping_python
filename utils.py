import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

import jwt
import datetime


from sqlalchemy import create_engine, text


def get_engine():
    """Creating SQLite Engine to interact"""
    return create_engine("sqlite:///scrapingdb.db", future=True)


def run_query(query, commit: bool = False):
    """Runs a query against the given SQLite database.

    Args:
        commit: if True, commit any data-modification query (INSERT, UPDATE, DELETE)
    """
    engine = get_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]