from sqlalchemy import create_engine, text # Mengimport dari ORM SqlAlchemy

def get_engine():
    return create_engine("sqlite:///scrapingdb.db", future=True)


def run_query(query, commit: bool = False):
    engine = get_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]