import argparse
import json

from WeatherCheckerTools.main import WeatherHere


def __parse_args():
    parser = argparse.ArgumentParser(prog="WeatherCheckerTools",
                                     description="Checks weather at location")
    parser.add_argument("-f", "--inputpath", help="path to input JSON file containing data")
    parser.add_argument("-c", "--coordinates", nargs=2, type=float, metavar=('x', 'y'),
                        help="a tuple of x and y coordinates")
    parser.add_argument("-C", "--conditions", nargs='+', help="a list of conditions")
    parser.add_argument("-o", "--outputpath", help="path to the output JSON file")

    return parser.parse_args()


if __name__ == "__main__":
    parsed_args = __parse_args()

    output = "output.json"

    file = "input.json"

    if bool(parsed_args.inputpath):
        file = parsed_args.inputpath

    with open(file, "r", encoding="utf8") as inpt:
        inpt = json.loads(inpt.read())
        conditions = inpt["conditions"]
        coords = inpt["coords"]

    if bool(parsed_args.outputpath):
        output = parsed_args.outputpath

    if bool(parsed_args.conditions):
        conditions = parsed_args.conditions

    if bool(parsed_args.coordinates):
        coords = parsed_args.coordinates

    weather = WeatherHere()
    weather.init(conditions, coords, output)
    weather.write_json()