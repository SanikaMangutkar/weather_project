from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '81c5937c34e74c7fbad124820250607'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None

    if request.method == 'POST':
        city = request.form['city']
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['location']['name'],
                'temp': data['current']['temp_c'],
                'feels_like': data['current']['feelslike_c'],
                'condition': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'humidity': data['current']['humidity'],
                'wind': data['current']['wind_kph'],
                'forecast': [
                    {
                        'date': day['date'],
                        'avg_temp': day['day']['avgtemp_c'],
                        'condition': day['day']['condition']['text'],
                        'icon': day['day']['condition']['icon']
                    }
                    for day in data['forecast']['forecastday']
                ]
            }

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
