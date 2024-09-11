from flask import Flask, jsonify, request
from pymongo import MongoClient
import stanza

app = Flask(__name__)

# Initialize Stanza NLP pipeline for Arabic
nlp = stanza.Pipeline(lang='ar', processors='tokenize,ner')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['article_database']  # Replace with your actual database name
collection = db['articles']  # Replace with your actual collection name


@app.route('/extract_entities', methods=['GET'])
def extract_entities():
    for article in collection.find():
        if 'full_text' in article and article['full_text']:
            try:
                # Perform NER using Stanza
                doc = nlp(article['full_text'])
                entities = [{'text': ent.text, 'type': ent.type} for ent in doc.ents]

                # Update the article with the extracted entities
                collection.update_one({'_id': article['_id']}, {'$set': {'entities': entities}})
                print(f"Extracted entities for article {article['_id']}: {entities}")  # Log entities

            except Exception as e:
                # Print the error message for debugging
                print(f"Error processing article {article['_id']}: {e}")

    return jsonify({"status": "Entities extracted and stored"}), 200


@app.route('/articles_by_entity/<entity>', methods=['GET'])
def articles_by_entity(entity):
    # Query articles where 'text' field inside 'entities' matches the specified entity
    articles = collection.find({'entities': {'$elemMatch': {'text': {'$regex': entity, '$options': 'i'}}}})

    results = []
    for article in articles:
        # Filter out entities where 'text' matches the searched entity
        matching_entities = [ent for ent in article.get('entities', []) if entity in ent.get('text', '')]

        # Append only article_id, title, and the matching entities
        results.append({
            "article_id": str(article['_id']),
            "title": article.get('title', 'No title'),
            "entities": [{"text": ent.get('text'), "type": ent.get('type')} for ent in matching_entities]
        })

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
