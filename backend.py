from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import csv

app = Flask(__name__)
CORS(app)

API_URL = "https://api.forexrateapi.com/v1/convert"
API_KEY="bbd5a356f9ac4b1b756adaa9d1b640bc"

@app.route('/')
def index():
    dropdown_options = []
    with open('static/data/currencies.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row: 
                dropdown_options.append(row[0]+" : "+row[1])
    return render_template('index.html', options=dropdown_options)


@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    from_currency = data.get("from", "").upper()
    to_currency   = data.get("to", "").upper()
    amount_str    = data.get("amount", "0")

    try:
        amount = float(amount_str)
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    params = {
        "api_key": API_KEY,
        "from":from_currency,
        "to":to_currency,
        "amount":amount_str 
    }

    response = requests.get(API_URL, params=params)
    
    result_json = response.json()
    success = result_json.get("success")

    if success == False:
        print("API ERROR:", result_json)
        return jsonify({"error": result_json}), 400

    return jsonify({"result": result_json.get('result')})


if __name__ == "__main__":
    app.run(debug=True)

