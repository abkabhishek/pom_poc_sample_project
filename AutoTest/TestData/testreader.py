"""
reader functions for all test data json
"""
import json


def get_hotel_list():
    """ function to get holels json as a list"""
    json_data = None
    with open("TestData/Hotel.json") as json_file:
        json_data = json.load(json_file)
        print(json_data)
        
    return json_data