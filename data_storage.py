import os
import json
import pymongo
from pymongo import MongoClient

class MongoDBUtility:
    def __init__(self, db_name='article_database', collection_name='articles'):
        # Establish a connection to the MongoDB server
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        if isinstance(data, list):
            self.collection.insert_many(data)
        else:
            self.collection.insert_one(data)
        print(f"Inserted {len(data) if isinstance(data, list) else 1} documents into the collection.")

    def close(self):
        self.client.close()

def load_json_files(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    articles = []

    for file_name in json_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            articles.extend(data)

    return articles

def main():
    # Specify the directory where the JSON files are stored
    directory =r'C:\Users\user\PycharmProjects\pythonProject1'

    # Load the articles from the JSON files
    articles = load_json_files(directory)

    # Initialize the MongoDB utility
    mongo_util = MongoDBUtility()

    # Insert the loaded articles into the MongoDB collection
    mongo_util.insert_data(articles)

    # Close the MongoDB connection
    mongo_util.close()

if __name__ == "__main__":
    main()
