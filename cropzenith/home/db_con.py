from pymongo import MongoClient

def con_db():
    client = MongoClient(
        host='localhost',
        port=27017,
        username='',
        password='',
        authSource='admin'
    )
    db = client['farmer']  # Replace with your actual database name
    return db




