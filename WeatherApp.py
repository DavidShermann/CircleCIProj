from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from countryinfo import CountryInfo
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.config['SECRET_KEY'] = '661a50e0edbb39371492d2a3518cb98b94c7b22efc972448c8'


def get_coords_by_name(name: str):
    """
    A function that receives a name of a city/country and
    returns a list which includes: longitude,latitude,city name and country name
    :param name:
    :return res_list:
    """
    real_country = ""
    real_city = ""
    newlocation = ""
    check_name = all(x.isalpha() or x.isspace() or " " in x for x in name)
    if check_name and name != "":
        name = name.title()
        geolocator = Nominatim(user_agent="My_App")
        try:
            location = CountryInfo(name).capital()
            newlocation = geolocator.geocode(location)
            real_country = name
            real_city = location
        except:
            newlocation = geolocator.geocode(name)
            if newlocation is not None:
                 real_city = name
                 real_country = \
                 geolocator.reverse(str(newlocation.latitude) + "," + str(newlocation.longitude), language='en').raw[
                        'address'].get('country', '')
            else:
                 return None
        res_list = [newlocation.longitude, newlocation.latitude, real_city, real_country]
        return res_list
    return None


def get_weather_data(cord1, cord2) -> list:
    """
    A function that receives coordination of a city/country and
    returns a formatted list of: dates,temperature average in day and night
    and humidity average in day and night for the next 7 days
    :param cord1:
    :param cord2:
    :return res_list:
    """
    long = cord1
    lat = cord2
    s = "https://api.open-meteo.com/v1/forecast?latitude=" + str(round(lat, 2)) + \
        "&longitude=" + str(round(long, 2)) + "&hourly=temperature_2m,relativehumidity_2m"
    p = requests.get(s).json()

    time = p["hourly"]["time"]
    temperature = p["hourly"]["temperature_2m"]
    humid = p["hourly"]["relativehumidity_2m"]

    time_list = []
    temp_day_avg = []
    temp_night_avg = []
    humid_day_avg = []
    humid_night_avg = []
    for i in range(7):
        time_list.append(time[0 + i * 24][0:10])
        temp_day, temp_night, humid_day, humid_night = 0, 0, 0, 0
        for j in range(12):
            if i != 6:
                temp_day += temperature[24 * i + j + 7]
                temp_night += temperature[24 * i + j + 19]
                humid_day += humid[24 * i + j + 7]
                humid_night += humid[24 * i + j + 19]
            else:
                temp_day += temperature[24 * i + j + 7]
                humid_day += humid[24 * i + j + 7]
                if j < 5:
                    temp_night += temperature[24 * i + j + 19]
                    humid_night += humid[24 * i + j + 19]
        if i != 6:
            temp_day_avg.append(round(temp_day / 12))
            temp_night_avg.append(round(temp_night / 12))
            humid_day_avg.append(round(humid_day / 12))
            humid_night_avg.append(round(humid_night / 12))
        else:
            temp_day_avg.append(round(temp_day / 12))
            temp_night_avg.append(round(temp_night / 5))
            humid_day_avg.append(round(humid_day / 12))
            humid_night_avg.append(round(humid_night / 5))

    res_list = []
    for i in range(len(time_list)):
        temp_date = time_list[i]
        parts = temp_date.split('-')
        temp_date = parts[2] + '-' + parts[1] + '-' + parts[0]
        time_list[i] = temp_date
        res_list.append(
            {
                "Time": time_list[i],
                "Temperature_At_Day": temp_day_avg[i],
                "Temperature_At_Night": temp_night_avg[i],
                "Humidity_At_Day": humid_day_avg[i],
                "Humidity_At_Night": humid_night_avg[i]
            }
        )
    return res_list


@app.route('/', methods=['GET'])
def landing_page():
    return render_template('landing_page.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather_page():
    if request.method == 'POST':
        name = request.form["text_box"]
        coords = get_coords_by_name(name)
        if coords is None:
            flash("Invalid City/Country Inserted!!!")
            return redirect(url_for('landing_page'))
        else:
            data = get_weather_data(coords[0], coords[1])
            return render_template('weather.html', data=data, names=(coords[2], coords[3]))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
