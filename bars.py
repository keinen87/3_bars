import json
import os
import sys

def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath,'r') as raw_json_file:
        return json.load(raw_json_file)


def get_biggest_bar(data):
    pass


def get_smallest_bar(data):
    pass


def get_closest_bar(data, longitude, latitude):
    pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        source_json = load_data(filepath)

    else:
        print("Error! Enter path!")
	
