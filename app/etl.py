import argparse
import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

from models import Base, Books

DB_URI = os.getenv("DB_URI")
DATA_PATH = "./dataset/"


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


def load_data_into_books_table(data: list, session: sessionmaker()) -> None:

    insert_statement = insert(Books).values(data).on_conflict_do_nothing()
    session.execute(insert_statement)
    session.commit()


if __name__ == "__main__":
    logger = get_module_logger(__name__)
    args = define_args()
    file_path = f"{DATA_PATH}{args.file_name}"
    logger.info(f"Extracting data from {file_path}")
    data = extract_and_transform_csv(file_path)
    session = create_session(DB_URI)

    try:
        logger.info("Loading data into the database...")
        load_data_into_books_table(data, session)
    except Exception as e:
        session.rollback()
        logger.error(e)
        logger.info("Rolling back changes...")

    finally:
        session.close()
        logger.info("Session closed. Exiting...")
