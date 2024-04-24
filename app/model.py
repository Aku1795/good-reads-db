from sqlalchemy import Column, Date, String, Integer, Double, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Books(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    title = Column(String(60), unique=True)
    authors = Column(String(60))
    average_rating = Column(Double)
    isbn = Column(Integer)
    language_code = Column(String(10))
    num_pages = Column(Integer)
    ratings_count = Column(Integer)
    text_reviews_count = Column(Integer)
    publication_date = Column(Date)
    publisher = Column(String(60))

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"