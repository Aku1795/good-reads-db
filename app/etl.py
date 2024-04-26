import argparse
import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Books

DB_URI = os.getenv("DB_URI")
DATA_PATH = "./dataset/"


def define_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_name", default="books.csv", help="The name of the file to be loaded")
    return parser.parse_args()


def extract_and_transform_csv(file_path: str) -> pd.DataFrame:
    # Extract
    logging.info(f"Extracting data from {file_path}")
    df = pd.read_csv(file_path, on_bad_lines='skip')

    # Transform
    logging.info("Transforming data...")
    df = df.rename(columns={"  num_pages": "num_pages"})

    return df.to_dict(orient="records")


def create_session(db_uri: str) -> sessionmaker():

    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    session = sessionmaker()
    session.configure(bind=engine)

    return session()


def load_data_into_books_table(data: list, session: sessionmaker()) -> None:
    logging.info("Loading data into the database...")
    for row in data:
        record = Books(**{
            "isbn": row["isbn13"],
            "title": row["title"],
            "authors": row["authors"],
            "average_rating": row["average_rating"],
            "language_code": row["language_code"],
            "num_pages": row["num_pages"],
            "ratings_count": row["ratings_count"],
            "text_reviews_count": row["text_reviews_count"],
            "publication_date": row["publication_date"],
            "publisher": row["publisher"],
        })
        session.add(record)

    logging.info("Data loaded successfully, commiting changes...")

    session.commit()


if __name__ == "__main__":
    args = define_args()
    file_path = f"{DATA_PATH}{args.file_name}"
    data = extract_and_transform_csv(file_path)[5:11]
    session = create_session(DB_URI)

    try:
        load_data_into_books_table(data, session)
    except Exception as e:
        session.rollback()

        logging.error(e)
        logging.info("Rolling back changes...")

    finally:
        session.close()

        logging.info("Session closed. Exiting...")
