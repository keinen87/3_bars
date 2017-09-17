import json
import os
import sys
from collections import Counter
from haversine import haversine
from math import radians, cos, sin, asin, sqrt


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as raw_json_file:
        return json.load(raw_json_file)


def get_biggest_bar(data):
    seatscounts = []
    target_bars = []
    for i in data['features']:
        seatscounts.append(i['properties']['Attributes']['SeatsCount'])
    for i in range(len(data['features'])):
        if data['features'][i]['properties']['Attributes']['SeatsCount'] == max(seatscounts):
            target_bars.append(data['features'][i]['properties']['Attributes']['Name'])
    return target_bars


def get_smallest_bar(data):
    seatscounts = []
    target_bars = []
    for i in data['features']:
        seatscounts.append(i['properties']['Attributes']['SeatsCount'])
    for i in range(len(data['features'])):
        if data['features'][i]['properties']['Attributes']['SeatsCount'] == min(seatscounts):
            target_bars.append(data['features'][i]['properties']['Attributes']['Name'])
    return target_bars


def min_unique(dictionary):
    minval, result = float('inf'), None
    counter = Counter(dictionary.values())
    for key, val in dictionary.items():
        if (val < minval) and (counter[val] == 1):
            minval = val
            result = key
    return key

def get_closest_bar(data, longitude, latitude):
    current = (latitude, longitude)
    coordinates = {data['features'][i]['properties']['Attributes']['Name']: tuple(list(reversed(data['features'][i]['geometry']['coordinates']))) for i in range(len(data['features'])) }
    haversine_pool = {key: haversine(coordinates[key],current) for key in coordinates }
    return min_unique(haversine_pool)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        source_json = load_data(filepath) #data = load_data('/home/nurbek/Загрузки/bars.json')
        print('Самые большие бары: ',get_biggest_bar(source_json))
        print('Самые маленькие бары: ',get_smallest_bar(source_json))
        print('Самый близкий бар: ',get_closest_bar(source_json, float(input('Enter longitude: ')),float(input('Enter latitude: '))))
    else:
        print("Error! Enter path!")
