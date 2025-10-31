from flask import Flask, render_template, jsonify
import weatherapi
from weatherapi.rest import ApiException
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def main():
    return render_template("index.html")

@app.route("/get_data")
def get_data():
    configuration = weatherapi.Configuration()
    configuration.api_key['key'] = os.getenv("WEATHER_API")
    
    api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration=configuration))
    
    city = "Jaipur"
    
    try:
        response = api_instance.realtime_weather(city)
        print(response)
    except ApiException as e:
        print("Exception occured")
    
    return jsonify({
        "name": "Devadyumna",
        "ID": 1
    })

if __name__ == "__main__":
    app.run(debug=True)