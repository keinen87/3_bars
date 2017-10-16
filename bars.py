import argparse
import json
import sys
from collections import Counter
from haversine import haversine


def load_data(filepath):
    with open(filepath, 'r') as raw_json_file:
        return json.load(raw_json_file)


def get_biggest_bars(json_data):
    seatscounts = [i['properties']['Attributes']['SeatsCount']
                   for i in json_data['features']]

    target_bars = [i['properties']['Attributes']['Name']
                   for i in json_data['features']
                   if i['properties']['Attributes']['SeatsCount'] ==
                   max(seatscounts)
                   ]
    return target_bars


def get_smallest_bars(json_data):
    seatscounts = [i['properties']['Attributes']['SeatsCount']
                   for i in json_data['features']]
    target_bars = [i['properties']['Attributes']['Name']
                   for i in json_data['features']
                   if i['properties']['Attributes']['SeatsCount'] ==
                   min(seatscounts)
                   ]
    return target_bars


def min_unique(dictionary):
    minval = float('inf')
    counter = Counter(dictionary.values())
    for key, val in dictionary.items():
        if (val < minval) and (counter[val] == 1):
            minval = val
    return key


def get_closest_bar(json_data, longitude, latitude):
    current = (latitude, longitude)
    coordinates = {i['properties']['Attributes']['Name']:
                   i['geometry']['coordinates'][::-1]
                   for i in json_data['features']}
    haversine_pool = {key: haversine(coordinates[key], current)
                      for key in coordinates}
    return min_unique(haversine_pool)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='Path to file')
    args = parser.parse_args()
    filepath = args.filepath    
    source_json = load_data(filepath)
    print('Самые большие бары: ', get_biggest_bars(source_json))
    print('Самые маленькие бары: ', get_smallest_bars(source_json))
    print('Самый близкий бар: ',
          get_closest_bar(source_json,
                          float(input('Enter longitude: ')),
                          float(input('Enter latitude: '))))
