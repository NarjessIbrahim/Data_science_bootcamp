from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['article_database']
collection = db['articles']


# Endpoint for Top Keywords
@app.route('/top_keywords', methods=['GET'])
def top_keywords():
    pipeline = [
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['_id']} ({item['count']} occurrences)" for item in result]

    return jsonify(formatted_result)


# Endpoint for Top Authors
@app.route('/top_authors', methods=['GET'])
def top_authors():
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)


# Endpoint for Articles by Publication Date
@app.route('/articles_by_date', methods=['GET'])
def articles_by_date():
    pipeline = [
        {
            "$addFields": {
                "published_date": {
                    "$dateFromString": {"dateString": "$published_time"}
                }
            }
        },
        {
            "$project": {
                "published_date": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$published_date"}
                }
            }
        },
        {
            "$group": {
                "_id": "$published_date",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "date": "$_id",
                "count": 1,
                "_id": 0
            }
        },
        {
            "$sort": {"date": 1}  # Sort by date in ascending order
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['date']} ({item['count']} articles)" for item in result]

    return jsonify(formatted_result)


# Endpoint for Articles by Word Count
@app.route('/articles_by_word_count', methods=['GET'])
def articles_by_word_count():
    pipeline = [
        {
            "$group": {
                "_id": "$word_count",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "word_count": "$_id",
                "article_count": "$count",
                "_id": 0
            }
        },
        {
            "$sort": {"word_count": 1}  # Sort by word count in ascending order
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['word_count']} words ({item['article_count']} articles)" for item in result]

    return jsonify(formatted_result)


# Endpoint for Articles by Language
@app.route('/articles_by_language', methods=['GET'])
def articles_by_language():
    pipeline = [
        {
            "$group": {
                "_id": "$lang",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "language": "$_id",
                "article_count": "$count",
                "_id": 0
            }
        },
        {
            "$sort": {"article_count": -1}  # Sort by article count in descending order
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['language']} ({item['article_count']} articles)" for item in result]

    return jsonify(formatted_result)


# Endpoint for Articles by Category
@app.route('/articles_by_classes', methods=['GET'])
def articles_by_classes():
    pipeline = [
        {"$unwind": "$classes"},
        {
            "$group": {
                "_id": "$classes.value",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "category": "$_id",
                "article_count": "$count",
                "_id": 0
            }
        },
        {
            "$sort": {"article_count": -1}  # Sort by article count in descending order
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['category']} ({item['article_count']} articles)" for item in result]

    return jsonify(formatted_result)


# Endpoint for Recent Articles
@app.route('/recent_articles', methods=['GET'])
def recent_articles():
    pipeline = [
        {
            "$sort": {"published_time": -1}  # Sort by publication time in descending order
        },
        {
            "$limit": 10  # Limit to the 10 most recent articles
        },
        {
            "$project": {
                "title": 1,
                "published_time": 1,
                "_id": 0
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['title']} (Published on {item['published_time']})" for item in result]

    return jsonify(formatted_result)


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
