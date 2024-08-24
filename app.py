
from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

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


# Endpoint for Articles by Keyword
@app.route('/articles_by_keyword/<keyword>', methods=['GET'])
def articles_by_keyword(keyword):
    pipeline = [
        {"$match": {"keywords": keyword}},
        {"$project": {"title": 1, "_id": 0}},
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [item['title'] for item in result]

    return jsonify(formatted_result)

# Endpoint for Articles by Author
@app.route('/articles_by_author/<author_name>', methods=['GET'])
def articles_by_author(author_name):
    pipeline = [
        {"$match": {"author": author_name}},
        {"$project": {"title": 1, "_id": 0}},
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [item['title'] for item in result]

    return jsonify(formatted_result)

# Endpoint for Top Classes
@app.route('/top_classes', methods=['GET'])
def top_classes():
    pipeline = [
        {"$unwind": "$classes"},
        {"$group": {"_id": "$classes.value", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {
            "$project": {
                "class": "$_id",
                "article_count": "$count",
                "_id": 0
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['class']} ({item['article_count']} articles)" for item in result]

    return jsonify(formatted_result)

# Endpoint for Article Details
@app.route('/article_details/<postid>', methods=['GET'])
def article_details(postid):
    result = collection.find_one({"post_id": postid}, {"_id": 0, "url": 1, "title": 1, "keywords": 1})

    if result:
        formatted_result = {
            "URL": result.get("url"),
            "Title": result.get("title"),
            "Keywords": result.get("keywords", [])
        }
        return jsonify(formatted_result)
    else:
        return

# Endpoint for Articles Containing Video
@app.route('/articles_with_video', methods=['GET'])
def articles_with_video():
    pipeline = [
        {"$match": {"video_duration": {"$ne": None}}},  # Filter articles where video_duration is not null
        {"$project": {"title": 1}},  # Project only the title field
        {"$sort": {"title": 1}}  # Sort by title in ascending order (optional)
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [item['title'] for item in result]

    return jsonify(formatted_result)


# Endpoint for Articles by Publication Year
@app.route('/articles_by_year/<int:year>', methods=['GET'])
def articles_by_year(year):
    pipeline = [
        {
            "$addFields": {
                "published_year": {
                    "$year": {"date": {"$dateFromString": {"dateString": "$published_time"}}}
                }
            }
        },
        {
            "$match": {"published_year": year}
        },
        {
            "$group": {
                "_id": "$published_year",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "year": "$_id",
                "article_count": "$count",
                "_id": 0
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    if result:
        formatted_result = [f"{item['year']} ({item['article_count']} articles)" for item in result]
        return jsonify(formatted_result)
    else:
        return jsonify({"error": "No articles found for the specified year"}), 404


# Endpoint for Longest Articles
@app.route('/longest_articles', methods=['GET'])
def longest_articles():
    pipeline = [
        {
            "$sort": {"word_count": -1}  # Sort by word count in descending order
        },
        {
            "$limit": 10  # Limit to the top 10 longest articles
        },
        {
            "$project": {
                "title": 1,
                "word_count": 1,
                "_id": 0
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['title']} ({item['word_count']} words)" for item in result]

    return jsonify(formatted_result)



# Endpoint for Shortest Articles
@app.route('/shortest_articles', methods=['GET'])
def shortest_articles():
    pipeline = [
        {
            "$sort": {"word_count": 1}  # Sort by word count in ascending order
        },
        {
            "$limit": 10  # Limit to the top 10 shortest articles
        },
        {
            "$project": {
                "title": 1,
                "word_count": 1,
                "_id": 0
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['title']} ({item['word_count']} words)" for item in result]

    return jsonify(formatted_result)


# Endpoint for Articles by Keyword Count
@app.route('/articles_by_keyword_count', methods=['GET'])
def articles_by_keyword_count():
    pipeline = [
        {
            "$project": {
                "keyword_count": {"$size": "$keywords"}  # Count the number of keywords
            }
        },
        {
            "$group": {
                "_id": "$keyword_count",
                "article_count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "keywords": "$_id",
                "article_count": "$article_count",
                "_id": 0
            }
        },
        {
            "$sort": {"keywords": 1}  # Sort by keyword count in ascending order
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['keywords']} keywords ({item['article_count']} articles)" for item in result]

    return jsonify(formatted_result)


# Endpoint for Articles with Thumbnail
@app.route('/articles_with_thumbnail', methods=['GET'])
def articles_with_thumbnail():
    pipeline = [
        {
            "$match": {"thumbnail": {"$ne": None}}  # Filter articles where thumbnail is not null
        },
        {
            "$project": {
                "title": 1  # Project only the title field
            }
        },
        {
            "$sort": {"title": 1}  # Sort by title in ascending order (optional)
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [item['title'] for item in result]

    return jsonify(formatted_result)

# Endpoint for Articles Updated After Publication
@app.route('/articles_updated_after_publication', methods=['GET'])
def articles_updated_after_publication():
    pipeline = [
        {
            "$match": {
                "$expr": {
                    "$gt": ["$last_updated", "$published_time"]  # Check if last_updated is after published_time
                }
            }
        },
        {
            "$project": {
                "title": 1,  # Include the title in the results
                "_id": 0
            }
        },
        {
            "$sort": {"title": 1}  # Optional: Sort by title in ascending order
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['title']} (Last updated after publication)" for item in result]

    return jsonify(formatted_result)


# Endpoint for Articles by Coverage
@app.route('/articles_by_coverage/<coverage>', methods=['GET'])
def articles_by_coverage(coverage):
    pipeline = [
        {
            "$unwind": "$classes"  # Unwind the classes array to filter on individual class items
        },
        {
            "$match": {
                "classes.value": coverage  # Match articles with the specified coverage category
            }
        },
        {
            "$project": {
                "title": 1,  # Include the title in the results
                "_id": 0
            }
        },
        {
            "$sort": {"title": 1}  # Optional: Sort by title in ascending order
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['title']} (Coverage on {coverage})" for item in result]

    return jsonify(formatted_result)


# Endpoint for Articles by Word Count Range
@app.route('/articles_by_word_count_range/<int:min>/<int:max>', methods=['GET'])
def articles_by_word_count_range(min, max):
    # MongoDB query to find articles within the specified word count range
    query = {
        "word_count": {
            "$gte": min,
            "$lte": max
        }
    }

    # Execute the query
    articles = list(collection.find(query, {"title": 1, "word_count": 1, "_id": 0}))

    # Count the number of articles found
    article_count = len(articles)

    # Check if any articles were found
    if not articles:
        return jsonify({"message": "No articles found in the specified word count range."}), 404

    # Format the response
    response_message = f"Articles between {min} and {max} words ({article_count} articles)"

    return jsonify({"message": response_message})



# Endpoint for Articles with Specific Keyword Count
@app.route('/articles_with_specific_keyword_count/<int:count>', methods=['GET'])
def articles_with_specific_keyword_count(count):
    # MongoDB query to find articles with exactly the specified number of keywords
    query = {
        "keywords": {
            "$size": count
        }
    }

    # Execute the query
    articles = list(collection.find(query, {"title": 1, "keywords": 1, "_id": 0}))

    # Count the number of articles found
    article_count = len(articles)

    # Check if any articles were found
    if not articles:
        return jsonify({"message": f"No articles found with exactly {count} keywords."}), 404

    # Format the response
    response_message = f"Articles with exactly {count} keywords ({article_count} articles)"

    return jsonify({"message": response_message})


# Endpoint for Articles Containing Specific Text
@app.route('/articles_containing_text/<text>', methods=['GET'])
def articles_containing_text(text):
    # Query to find articles that contain the specific text within their content (full_text)
    query = {
        "full_text": {
            "$regex": text,
            "$options": "i"  # Case-insensitive search
        }
    }

    # Execute the query
    articles = list(collection.find(query, {"title": 1, "_id": 0}))

    # Format the response message
    response_message = f'Articles containing "{text}"'

    # List all article titles found
    article_titles = [article['title'] for article in articles]

    # Prepare the response
    response = {
        "message": response_message,
        "articles": article_titles
    }

    return jsonify(response)


# Endpoint for Articles with More than N Words
@app.route('/articles_with_more_than/<int:word_count>', methods=['GET'])
def articles_with_more_than(word_count):
    # Query to find articles with more than the specified number of words
    query = {
        "word_count": {
            "$gt": word_count
        }
    }

    # Execute the query and count the number of matching articles
    article_count = collection.count_documents(query)

    # Format the response message
    response_message = f"Articles with more than {word_count} words ({article_count} articles)"

    # Prepare the response
    response = {
        "message": response_message
    }

    return jsonify(response)


# Endpoint for Articles Grouped by Coverage
@app.route('/articles_grouped_by_coverage', methods=['GET'])
def articles_grouped_by_coverage():
    # Aggregation pipeline to group articles by the coverage category in the 'classes' field
    pipeline = [
        {
            "$unwind": "$classes"
        },
        {
            "$match": {
                "classes.mapping": "coverage"
            }
        },
        {
            "$group": {
                "_id": "$classes.value",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]

    # Execute the aggregation pipeline
    results = collection.aggregate(pipeline)

    # Format the response
    response = {}
    for result in results:
        coverage_category = result['_id']
        count = result['count']
        response[f"Coverage on {coverage_category}"] = f"({count} articles)"

    return jsonify(response)


# Endpoint for Articles by Length of Title
@app.route('/articles_by_title_length', methods=['GET'])
def articles_by_title_length():
    # Aggregation pipeline to get titles and their lengths
    pipeline = [
        {
            "$project": {
                "title_length": {
                    "$size": {
                        "$split": ["$title", " "]  # Splitting title into words to count length
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$title_length",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"_id": 1}  # Sort by title length
        }
    ]

    # Execute the aggregation pipeline
    results = list(collection.aggregate(pipeline))

    # Format the response
    response = {f"Titles with {item['_id']} words": f"{item['count']} articles" for item in results}

    return jsonify(response)


# Endpoint for Most Popular Keywords in the Last X Days
@app.route('/popular_keywords_last_X_days', methods=['GET'])
def popular_keywords_last_X_days():
    # Get the number of days from the query parameters
    days = int(request.args.get('days', 7))  # Default to 7 days if not provided

    # Calculate the start date
    end_date = datetime.now(pytz.utc)
    start_date = end_date - timedelta(days=days)

    # Convert dates to ISO format for comparison
    start_date_iso = start_date.isoformat()
    end_date_iso = end_date.isoformat()

    # Define the pipeline for aggregation
    pipeline = [
        {
            "$match": {
                "published_time": {
                    "$gte": start_date_iso,
                    "$lte": end_date_iso
                }
            }
        },
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    result = list(collection.aggregate(pipeline))

    # Format the results
    formatted_result = [f"{item['_id']} ({item['count']} occurrences)" for item in result]

    return jsonify(formatted_result)


@app.route('/articles_by_specific_date/<date>', methods=['GET'])
def articles_by_specific_date(date):
    try:
        # Convert the input date to a datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d')

        # Create a start and end of the day for querying
        start_of_day = datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0, tzinfo=pytz.UTC)
        end_of_day = start_of_day.replace(hour=23, minute=59, second=59)

        # Query the collection for articles published on that specific date
        query = {
            'published_time': {
                '$gte': start_of_day.isoformat(),
                '$lte': end_of_day.isoformat()
            }
        }
        articles = list(collection.find(query))
        count = len(articles)

        return jsonify({date: count})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/articles_by_month/<year>/<month>', methods=['GET'])
def articles_by_month(year, month):
    try:
        # Convert year and month to integers
        year = int(year)
        month = int(month)

        # Determine the start and end of the month
        start_of_month = datetime(year, month, 1, 0, 0, 0, tzinfo=pytz.UTC)
        end_of_month = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        # Query the collection for articles published in the given month
        query = {
            'published_time': {
                '$gte': start_of_month.isoformat(),
                '$lt': end_of_month.isoformat()
            }
        }
        count = collection.count_documents(query)

        # Format month name
        month_name = start_of_month.strftime('%B %Y')

        return jsonify({month_name: count})

    except Exception as e:
        return jsonify({"error": str(e)})


from pymongo.errors import ServerSelectionTimeoutError


@app.route('/most_updated_articles', methods=['GET'])
def most_updated_articles():
    try:
        pipeline = [
            # Add a field to count the number of updates
            {
                "$addFields": {
                    "update_count": {
                        "$size": {
                            "$ifNull": ["$update_history", []]
                        }
                    }
                }
            },
            # Group by article title and count the updates
            {
                "$group": {
                    "_id": "$title",
                    "update_count": {"$max": "$update_count"}
                }
            },
            # Sort by update_count in descending order
            {
                "$sort": {"update_count": -1}
            },
            # Limit to top 10 articles
            {
                "$limit": 10
            }
        ]

        # Execute the aggregation pipeline
        results = list(collection.aggregate(pipeline))

        # Format the response
        response = [{"title": result['_id'], "update_count": result['update_count']} for result in results]

        return jsonify(response)

    except ServerSelectionTimeoutError:
        return jsonify({"error": "Could not connect to MongoDB."}), 500



@app.route('/articles_last_X_hours', methods=['GET'])
def articles_last_x_hours():
    try:
        # Get the number of hours from the query parameter
        hours = int(request.args.get('hours', 24))  # Default to 24 hours if not provided

        # Calculate the start time for the query
        now = datetime.now(pytz.UTC)
        start_time = now - timedelta(hours=hours)

        # Query the collection for articles published in the last X hours
        query = {
            'published_time': {
                '$gte': start_time.isoformat()
            }
        }
        articles = collection.find(query)

        # Format the result
        results = []
        for article in articles:
            # Assuming there's a field 'title' for the article name
            title = article.get('title', 'Untitled')
            published_time = article.get('published_time')
            results.append(f"{title} (Published within the last {hours} hours)")

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})



#start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
