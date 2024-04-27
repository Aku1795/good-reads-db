import os
from etl import *
from models.models import Books

DB_URI = os.getenv("DB_URI")
DATA_PATH = "./dataset/"

def main() -> None:
    logger = get_module_logger(__name__)
    args = define_args()
    file_path = f"{DATA_PATH}{args.file_name}"
    logger.info(f"Extracting data from {file_path}")
    data = extract_and_transform_csv(file_path)
    session = create_session(DB_URI)

    try:
        logger.info("Loading data into the database...")
        load_data_into_books_table(data, Books, session)
    except Exception as e:
        session.rollback()
        logger.error(e)
        logger.info("Rolling back changes...")

    finally:
        session.close()
        logger.info("Session closed. Exiting...")


if __name__ == "__main__":
    main()