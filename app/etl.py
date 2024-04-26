import argparse
import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Books


DB_URI = os.getenv("DB_URI")
import subprocess

subprocess.run(["ls", "-l"])

def load_and_format_csv_to_list_of_dict(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_name, on_bad_lines='skip')
    df["num_pages"] = df["  num_pages"]
    df = df.drop(columns=["  num_pages"])
    return df.to_dict(orient="records")

def define_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", default="./dataset/books.csv", help="The name of the file to be loaded")
    return parser.parse_args()

if __name__ == "__main__":
    args = define_args()


    #Create the database
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    try:
        data = load_and_format_csv_to_list_of_dict(args.file_path)[:5]

        print(data)

        # for row in data:
        #     record = Books(**{
        #         "isbn": row["isbn13"],
        #         "title": row["title"],
        #         "authors": row["authors"],
        #         "average_rating": row["average_rating"],
        #         "language_code": row["language_code"],
        #         "num_pages": row["num_pages"],
        #         "ratings_count": row["ratings_count"],
        #         "text_reviews_count": row["text_reviews_count"],
        #         "publication_date": row["publication_date"],
        #         "publisher": row["publisher"],
        #     })
        #     s.add(record)


        logging.info("Data loaded successfully, commiting changes...")

        s.commit()
    except Exception as e:
        s.rollback()

        logging.error("An error occurred, rolling back changes...")

        logging.error(e.message)
    finally:
        s.close()

        logging.info("Session closed. Exiting...")
