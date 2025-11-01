from flask import Flask, render_template, jsonify, request, redirect, url_for
from weatherapi.rest import ApiException
import weatherapi
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Global Configuration ---
app = Flask(__name__)
# The CITY variable will hold the user's last search and must be defined globally
CITY = ""


@app.route("/")
@app.route("/home")
def main():
    """Renders the main page and passes the currently selected city for display."""
    global CITY
    return render_template("index.html", current_city=CITY)

@app.route("/fetch_city", methods = ['POST'])
def fetch_city():
    """Handles the form submission and updates the global CITY variable."""
    # NOTE: 'global' keyword is required to modify a variable outside the current scope
    global CITY 
    
    if request.method == 'POST':
        city = request.form.get("city_input")
        
        # Check if city is empty or just whitespace
        # NOTE: Corrected len(city.strip) to len(city.strip())
        if not city or len(city.strip()) == 0:
            # Return to home with an error parameter (optional, could be done via flash messages too)
            return redirect(url_for('main', error_message="Please enter a valid city name."))
        
        CITY = city.strip()
        
    # Redirect to the home page so the JavaScript can immediately fetch the new weather data
    return redirect(url_for('main'))

@app.route("/get_data")
def get_data():
    """Fetches real-time weather data for the stored city and returns it as JSON."""
    configuration = weatherapi.Configuration()
    configuration.api_key['key'] = os.getenv("WEATHER_API")

    # Initialize the API client instance
    try:
        api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration=configuration))
        
    except Exception as e:
        print(f"Error initializing WeatherAPI client: {e}")
        api_instance = None
    
    global CITY
    city = CITY
    
    if not api_instance:
        print("API client issue")
        return jsonify({"error": "API Client not initialized."}), 500
        
    if not city:
        # If no city has been set yet, return an empty response or prompt
        return jsonify({"message": "No city set. Use the form to enter a location."}), 200
        
    try:
        # Call the WeatherAPI
        # The API response is already dict-like, perfect for direct use
        response = api_instance.realtime_weather(city)
        
        print(response)
        
        location = response['location']
        current = response['current']
        condition = current['condition']
        
        current_data = {
            "name": location['name'],
            "region": location['region'],
            "temp": current['temp_c'],
            "day": "day" if current['is_day'] == 1 else "night",
            "condition_text": condition['text'],
            "condition_icon": condition['icon'],
            "feels": current['feelslike_c']
        }
        
        return jsonify(current_data)
        
    except ApiException as e:
        # Catch API errors (e.g., city not found, invalid API key)
        error_message = f"Weather API Error: {e.reason}"
        if "No matching location found" in str(e):
            error_message = f"Location '{city}' not found. Please try again."
        
        # Return a JSON error response with an appropriate status code
        return jsonify({"error": error_message}), 400
        
    except Exception as e:
        # Catch other exceptions
        print(f"Random exception: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
