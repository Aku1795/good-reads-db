from sqlalchemy import Column, Date, String, Integer, Double, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Books(Base):
    __tablename__ = "books"

    isbn = Column(BigInteger, primary_key=True)
    title = Column(String)
    authors = Column(String)
    average_rating = Column(Double)
    language_code = Column(String)
    num_pages = Column(Integer)
    ratings_count = Column(Integer)
    text_reviews_count = Column(Integer)
    publication_date = Column(Date)
    publisher = Column(String)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"