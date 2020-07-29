import json
import requests
from sys import argv

script, stn_name = argv

def func_stn(stn_name):
    response_KIAD = requests.get(f'https://api.weather.gov/stations/{stn_name}')
    station_data = response_KIAD.json()
    forecast = station_data['properties']['forecast']
    first_line = station_data['properties']['name']
    coordinate = station_data['geometry']['coordinates']
    longitude = coordinate[0]
    latitude = coordinate [1]
    data_weather = requests.get(f'https://api.weather.gov/points/{latitude},{longitude}')
    forecast_link = data_weather.json()
    forecast_link_final = forecast_link ['properties']['forecastHourly']
    final_link = requests.get(f'{forecast_link_final}')
    final_link_json = final_link.json()
    temper_final = final_link_json ['properties']['periods']
    with open('sample.txt','w') as f:
        for data in temper_final:
            descr = data ['shortForecast']
            temp = str(data ['temperature'])
            wnd_spd = data['windSpeed']
            wnd_dirn = data['windDirection']
            f.write(descr)
            f.write('\n')
            f.write(temp)
            f.write('\n')
            f.write(wnd_spd)
            f.write('\n')
            f.write(wnd_dirn)
            f.write('\n')
    first_line = station_data['properties']['name']
    fifth_line = forecast_link ['properties']['relativeLocation']['properties']['bearing']['value']
    with open ('sample.txt', 'r') as f:
        linelist = f.readlines()
        dirn = direction (linelist[3])
        extract_line = linelist[0] + linelist[1] + linelist[2].replace('mph','') + dirn
        output = extract_line
    with open ('file_2.txt', 'w') as out_f2:
        out_f2.write(output)
    with open('file_2.txt') as f:
        data = f.readlines()
        second_line = data[0].strip()
        third_line = data[1].strip()
        third_line = round((float(third_line)-32)*(5/9),2)
        fourth_line = data[2].strip()
        fourth_line = round(float(fourth_line)*0.44704,2)
        sixth_line = dirn
    print(f'Station: {first_line}')
    print(f'Description: {second_line}')
    print(f'Temperature: {third_line} degC')
    print(f'Wind Speed: {fourth_line} m_s-1')
    print(f'Wind Direction: {sixth_line} degree_(angle)')

def direction(ltr):
    if ltr == 'E':
        return '0'
    elif ltr == 'N':
        return '90'
    elif ltr == 'NE' or 'EN':
        return '45'
    elif ltr == W:
        return '180'
    elif ltr == 'NW' or 'WN':
        return '135'
    elif ltr == S:
        return '270'
    elif ltr == 'SW' or 'WS':
        return '225'
    elif ltr == 'SE' or 'ES':
        return '315'

if stn_name == 'KIAD':
    func_stn(stn_name)

elif stn_name == "KDCA":
    func_stn(stn_name)
