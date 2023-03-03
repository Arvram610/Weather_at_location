""" A class that gets most accurate weather information based on location and specifications"""
import urllib
from typing import Optional
from urllib.request import urlopen
import json
import geopy.distance

from decode_weather import decoder
from key_conds import condition_to_key, key_to_conditions


class WeatherHere:
    """ The class in question"""
    def __init__(self):
        self.__coords = None
        self.__condition_keys = None
        self.__conditions = None
        self.__data = None
        self.__stations = None
        self.weather_conditions = None

    def init(self, conditions: set, coords: tuple):
        """ Inits the class when you want to, you can initiate it yourself by running set_location()
         And running set_conditions() then finally running update_data()"""

        self.set_conditions(conditions)  # sets conditions
        self.set_location(coords)  # sets coords
        self.update_data()

    def __stations_with_conditions(self, data: dict, condition_keys: set) -> list[dict]:
        rel_stations = {}
        for condition in data["resource"]:  # Loop all all_conditions.json
            if condition["key"] in condition_keys:  # If the condition is wanted
                url = condition["link"][0]["href"]
                stations = self.__get_stations(url, condition["key"])  # Get stations
                for station in stations.values():
                    station_keys = rel_stations.keys()
                    if station["name"] in station_keys:  # Merge two of the same stations
                        key = key_to_conditions[condition["key"]]
                        station_temp = rel_stations[station["name"]]
                        station_conditions = station_temp["all_conditions.json"]
                        all_conditions = station["all_conditions.json"]
                        station_conditions = station_conditions.union(all_conditions)
                        rel_stations[station["name"]]["all_conditions.json"] = station_conditions
                        condition_url = station[key]
                        rel_stations[station["name"]][key] = condition_url
                    else:
                        rel_stations[station["name"]] = station
        return list(rel_stations.values())

    @staticmethod
    def __get_station_condition_value(condition: str, station: dict) -> Optional[dict]:
        newurl = station[condition][:-5]
        newurl += "/station/" + station["key"] + ".json"
        # storing the JSON response
        # from url in data
        with urlopen(newurl) as response:
            data = json.loads(response.read())
            newurl = (data["period"][0]["link"][0]["href"])[:-5] + "/data.json"
            try:
                with urlopen(newurl) as response2:
                    data = json.loads(response2.read())
                    station[condition] = data["value"][0]
                    return data["value"][0]
            except urllib.error.HTTPError:
                return None

    @staticmethod
    def __get_stations(url: str, condition_key: str) -> dict:
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

    def __station_distance(self, station: dict) -> float:
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
                    station_weather = self.__get_station_condition_value(condition, station)
                    if station_weather is None:
                        continue
                    self.weather_conditions[condition] = station_weather
                    self.weather_conditions[condition]["station"] = station["name"]
                    self.weather_conditions[condition]["distance"] = station["distance"]
                    break

    def set_conditions(self, conditions: set):
        """ Update the condition list and update the stations and weather"""
        self.__conditions = conditions  # Makes all_conditions.json available to class
        # Generates key values
        self.__condition_keys = {condition_to_key[condition] for condition in conditions}
        print("Set conditions to:", ", ".join(conditions))

    def set_location(self, coords: tuple):
        """ Update the location and update stations and weather"""
        self.__coords = coords
        print("Set location to:", tuple(coords))

    def update_data(self):
        """ Get new data"""
        self.__gen_data()  # Generate data
        self.__gen_stations()  # Generates stations
        self.__gen_weather()  # Generates weather for closest stations
        self.__decode_current_weather()
        print("Updated Data")

    def __decode_current_weather(self):
        """ Decodes the "Rådande Värder" value to a readable string"""
        if "Rådande väder" in self.weather_conditions:
            value = int(self.weather_conditions["Rådande väder"]["value"])
            self.weather_conditions["Rådande väder"]["value"] = decoder[value]["value"]

    def write_json(self):
        """ Writes data to json"""
        with open("output.json", "w") as outfile:
            json.dump(self.weather_conditions, outfile, ensure_ascii=False)
            print("Wrote to output.json")


if __name__ == "__main__":
    with open("input.json", "r") as inpt:
        inpt = json.loads(inpt.read())
        weather = WeatherHere()
        weather.init(inpt["conditions"], inpt["coords"])
        weather.write_json()
