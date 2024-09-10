import pymongo
from textblob import TextBlob
from flask import Flask, jsonify
from bson import ObjectId  # Import ObjectId to handle MongoDB object IDs

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["article_database"]
collection = db["articles"]


# Sentiment Analysis: Analyze all articles and update sentiment in MongoDB
def analyze_sentiment():
    for article in collection.find():
        # Check if 'full_text' exists and is not empty
        if 'full_text' in article and article['full_text']:
            analysis = TextBlob(article['full_text'])  # Analyze the full article text
            sentiment = analysis.sentiment.polarity  # Get polarity score (-1 to 1)
            # Update the article with the sentiment score in MongoDB
            collection.update_one({'_id': article['_id']}, {'$set': {'sentiment': sentiment}})
        else:
            print(f"Article with _id {article['_id']} has no full_text")


# Run sentiment analysis before starting the Flask app
analyze_sentiment()


# Function to serialize ObjectId to a string
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    return doc


# API to fetch articles by sentiment
@app.route('/articles_by_sentiment/<sentiment_type>', methods=['GET'])
def articles_by_sentiment(sentiment_type):
    query = {}
    if sentiment_type == 'positive':
        query = {"sentiment": {"$gt": 0}}
    elif sentiment_type == 'negative':
        query = {"sentiment": {"$lt": 0}}
    elif sentiment_type == 'neutral':
        query = {"sentiment": 0}

    result = list(collection.find(query))

    # Serialize ObjectId and other fields
    result = [serialize_doc(doc) for doc in result]

    return jsonify(result)


if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True)
