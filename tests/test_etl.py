from pandas import Timestamp

import app.etl as etl

FILE_PATH = './tests/mock_data/books.csv'

def test_extract_and_transform_csv():
    data = etl.extract_and_transform_csv(FILE_PATH)
    assert len(data) == 4
    assert data[0] == {
        'isbn': 9780439785969,
        'title': 'Harry Potter and the Half-Blood Prince (Harry Potter  #6)',
        'authors': 'J.K. Rowling/Mary GrandPré',
        'average_rating': 4.57,
        'language_code': 'eng',
        'num_pages': 652.0,
        'ratings_count': 2095690.0,
        'text_reviews_count': 27591,
        'publication_date': Timestamp('2006-09-16 00:00:00'),
        'publisher': 'Scholastic Inc.'
    }
