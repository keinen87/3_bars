import argparse
import json
from haversine import haversine


def load_data(filepath):
    with open(filepath, 'r') as raw_json_file:
        return json.load(raw_json_file)


def get_biggest_bar(json_data):
    return max(json_data,
               key=lambda bar: bar['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(json_data):
    return min(json_data,
               key=lambda bar: bar['properties']['Attributes']['SeatsCount'])


def get_closest_bar(json_data, longitude, latitude):
    current = (latitude, longitude)
    coordinates = {bar['properties']['Attributes']['Name']:
                   bar['geometry']['coordinates'][::-1]
                   for bar in json_data}
    haversine_pool = {key: haversine(coordinates[key], current)
                      for key in coordinates}
    return min(haversine_pool, key=lambda key: haversine_pool[key])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='Path to file')
    args = parser.parse_args()
    filepath = args.filepath
    bars_list = load_data(filepath)['features']
    biggest_bar = get_biggest_bar(bars_list)
    smallest_bar = get_smallest_bar(bars_list)
    closest_bar = get_closest_bar(bars_list,
                                  float(input('Enter longitude: ')),
                                  float(input('Enter latitude: ')))
    print('The biggest bar: ',
          biggest_bar["properties"]["Attributes"]["Name"])
    print('The samallest bar: ',
          smallest_bar["properties"]["Attributes"]["Name"])
    print('The closest bar: ', closest_bar)
