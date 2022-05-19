import  json, requests
from licenses import getWToken

def getWeatherMsg():


    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'

    API_KEY = getWToken()
    CITY = 'Merida'

    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY

    response = requests.get(URL)
    K = 273.15
    i = 0
    text = ''
    while i < 3:
        if response.status_code == 200:
            data = response.json()
            temp = data['main']
            weather = data['weather'][0]

            temp_min = temp['temp_min']-K
            temp_max = temp['temp_max']-K
            feel = temp['feels_like']-K
            
            main_w = weather['main']
            wth_r = weather['description']
            
            text = f'Merida - {main_w} with {wth_r}\n{temp_min:.1f}~{temp_max:.1f} feels like {feel:.1f}'

            return text
        else:
            print('Error obtaining weather data')

            i +=1
    print('Error getting weather data time out')


