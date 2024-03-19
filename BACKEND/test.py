from flask import Flask,  jsonify, request

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/auth', methods=['GET'])
def hello_world():
    user = request.args.get('q')
    password = request.args.get('password')
    print(f"USER: {user}  PASS: {password}")
    response = {"success": 1}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8080)
