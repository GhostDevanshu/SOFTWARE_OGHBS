from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://jainsujan031:b9dsO3WjqnhAe3bG@opensoftdb.8dhcszs.mongodb.net/?retryWrites=true&w=majority&appName=OpenSoftDB")
db = client.sample_mflix  # Replace "sample_mflix" with your actual database name
collection = db.movies  # Replace "movies" with your actual collection name


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# Test to search for data in the database
@app.route("/search")
def search_movies():
    query = request.args.get('q')
    print(query)
    db_result = collection.aggregate([
        {
            '$search': {
                'index': 'default',
                'text': {
                    'query': query,
                    'path': 'plot'
                }
            }
        }, {
            '$limit': 5
        },
        {
            '$project': {
                '_id': 0,
                'title': 1,
                'plot': 1,
            }
        }
    ])
    
    # Convert the result to a list before iterating over it
    results = []
    
    for movie in db_result:
        print(movie)
        results.append(movie['title'])
    
    response = {"results": results}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8080)