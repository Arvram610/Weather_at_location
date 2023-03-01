""" A class that gets most accurate weather information based on location and specifications"""

from urllib.request import urlopen

import sys

# import json
import json

import geopy.distance

from key_conds import *


class WeatherHere:
    """ The class in question"""
    def __init__(self, conditions, coords):
        self.__data = None
        self.__stations = None
        self.weather_conditions = None
        self.__conditions = conditions  # Makes all_conditions.json available to class
        # Generates key values
        self.__condition_keys = {condition_to_key[condition] for condition in conditions}

        self.__coords = coords  # Makes coords available to class

        self.update_data()

        self.write_json()

    def __stations_with_conditions(self, data, condition_keys):
        all_relevant_stations = {}
        for condition in data["resource"]:  # Loop all all_conditions.json
            if condition["key"] in condition_keys:  # If the condition is wanted
                url = condition["link"][0]["href"]
                stations = self.__get_stations(url, condition["key"])  # Get stations
                for station in stations.values():
                    station_keys = all_relevant_stations.keys()
                    if station["name"] in station_keys:  # Merge two of the same stations
                        key = key_to_conditions[condition["key"]]
                        station_temp = all_relevant_stations[station["name"]]
                        station_conditions = station_temp["all_conditions.json"]
                        station_conditions = station_conditions.union(station["all_conditions.json"])
                        all_relevant_stations[station["name"]]["all_conditions.json"] = station_conditions
                        condition_url = station[key]
                        all_relevant_stations[station["name"]][key] = condition_url
                    else:
                        all_relevant_stations[station["name"]] = station

        return list(all_relevant_stations.values())

    @staticmethod
    def __get_station_condition_value(condition, station):
        newurl = station[condition][:-5]
        newurl += "/station/" + station["key"] + ".json"
        # storing the JSON response
        # from url in data
        with urlopen(newurl) as response:
            data = json.loads(response.read())
            newurl = (data["period"][0]["link"][0]["href"])[:-5] + "/data.json"
            with urlopen(newurl) as response:
                data = json.loads(response.read())
                station[condition] = data["value"][0]
                return data["value"][0]

    @staticmethod
    def __get_stations(url, condition_key):
        stations = {}
        with urlopen(url) as response:
            # storing the JSON response
            # from url in data
            data = json.loads(response.read())
            for station in data["station"]:
                key = station["key"]
                if station["active"] and station["owner"] != "Icke namngiven ägare":
                    name = station["name"]
                    stations[name] = {"name": name,
                                      "all_conditions.json": {key_to_conditions[condition_key]},
                                      "longitude": station["longitude"],
                                      "latitude": station["latitude"],
                                      "key": key,
                                      key_to_conditions[condition_key]: url}
            return stations

    def __station_distance(self, station):
        long = station["longitude"]
        lat = station["latitude"]

        coords_1 = (lat, long)

        distance = geopy.distance.geodesic(coords_1, self.__coords).km

        station["distance"] = distance

        return distance

    def __gen_data(self):
        # store the URL in url as
        # parameter for urlopen
        url = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter.json"

        # store the response of URL
        with urlopen(url) as response:
            # storing the JSON response
            # from url in data
            self.__data = json.loads(response.read())

    def __gen_stations(self):
        self.__stations = self.__stations_with_conditions(self.__data, self.__condition_keys)
        self.__sort_stations()

    def __sort_stations(self):
        self.__stations.sort(key=self.__station_distance)

    def __gen_weather(self):
        self.weather_conditions = {}

        for condition in self.__conditions:
            for station in self.__stations:
                if condition in station["all_conditions.json"]:
                    weather = self.__get_station_condition_value(condition, station)
                    self.weather_conditions[condition] = weather
                    self.weather_conditions[condition]["station"] = station["name"]
                    self.weather_conditions[condition]["distance"] = station["distance"]
                    break

    def update_conditions(self, conditions):
        """ Update the condition list and update the stations and weather"""
        self.__conditions = conditions  # Makes all_conditions.json available to class
        # Generates key values
        self.__condition_keys = {condition_to_key[condition] for condition in conditions}
        self.__sort_stations()
        self.__gen_weather()
        self.write_json()

    def update_location(self, coords):
        """ Update the location and update stations and weather"""
        self.__coords = coords
        self.__sort_stations()
        self.__gen_weather()
        self.write_json()

    def update_data(self):
        """ Get new data if data is too old"""
        self.__gen_data()  # Generate data
        self.__gen_stations()  # Generates stations
        self.__gen_weather()  # Generates weather for closest stations
        self.write_json()

    def write_json(self):
        """ Writes data to json"""
        with open("output.json", "w") as outfile:
            json.dump(self.weather_conditions, outfile, ensure_ascii=False)




if __name__ == "__main__":
    with open("input.json", "r") as inpt:
        inpt = json.loads(inpt.read())
        WeatherHere(inpt["conditions"], inpt["coords"])
