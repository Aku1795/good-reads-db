import argparse
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

from models.models import Base

def get_module_logger(mod_name: str) -> logging.Logger:

    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def define_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file_name",
        default="books.csv",
        help="The name of the file to be loaded",
    )
    return parser.parse_args()


def extract_and_transform_csv(file_path: str) -> list[dict]:
    # Extract
    df = pd.read_csv(file_path, on_bad_lines="skip")

    # Transform
    df.drop("isbn", inplace=True, axis=1)
    df = df.rename(
        columns={
            "  num_pages": "num_pages",
            "isbn13": "isbn",
        }
    )
    df["publication_date"] = pd.to_datetime(
        df["publication_date"], errors="coerce", format="%m/%d/%Y"
    )

    df.dropna(subset=["publication_date"], inplace=True)

    SELECT = [
        "isbn",
        "title",
        "authors",
        "average_rating",
        "language_code",
        "num_pages",
        "ratings_count",
        "text_reviews_count",
        "publication_date",
        "publisher",
    ]
    df = df[SELECT]

    return df.to_dict(orient="records")


def create_session(db_uri: str) -> sessionmaker():

    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)

    return Session()


def load_data_into_books_table(data: list[dict], books_table, session: sessionmaker()) -> None:

    insert_statement = insert(books_table).values(data).on_conflict_do_nothing()
    session.execute(insert_statement)
    session.commit()



