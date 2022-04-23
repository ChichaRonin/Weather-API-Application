import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)

# declarative to specify the route to take on my flask application
# in this case it is the landing page/dashboard
@app.route('/')
def weather_dashboard():
    return render_template('landing_page.html')

# declarative to specify the route to results page once a user inputs a zip code
@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)

    # Formats JSON dictionary by parsing response to key values below
    # to render to the user
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('results_page.html', location=location, temp=temp, 
    feels_like=feels_like, weather=weather)

# Function to store configurations to specify my application and to store my api key
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

# Function to get weather results based on zip code, and my api key.
# Formatted to take in the parameters that user puts into the system
def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

if __name__ == '__main__':
    app.run()
