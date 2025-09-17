#### server.py:

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Добро пожаловать!</h1>'

@app.route('/calculate', methods=["POST"])
def calculate_balance():
    data = request.get_json()
    balance = int(data["income"]) - int(data["expenses"])
    return jsonify({"balance": balance})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


#### requirements.txt:


flask>=2.0.0
gunicorn>=20.0.0


#### Procfile (если вы используете Heroku):


web: gunicorn server:app
