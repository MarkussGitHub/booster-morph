import requests

degree_sign = u"\N{DEGREE SIGN}"
response = requests.get('http://api.weatherapi.com/v1/forecast.json?key=0e869fd7a75548bbaae212246201511&q=Riga').json()

def temperature():
    temperature = round(response['forecast']['forecastday'][0]['day']['avgtemp_c'])
    return '**{}{}C**'.format(temperature, degree_sign)

def rain_chance():
    rain_chance = response['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
    return '**{}{}**'.format(rain_chance, '%')

def snow_chance():
    snow_chance = response['forecast']['forecastday'][0]['day']['daily_chance_of_snow']
    return '**{}{}**'.format(snow_chance, '%')
