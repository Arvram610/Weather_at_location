""" The Rådande Väder value decoder"""
import json
from urllib.request import urlopen

URL = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/13/codes.json"
# store the URL in url as
# parameter for urlopen

# store the response of URL
with urlopen(URL) as response:
    # storing the JSON response
    # from url in data
    decoder = json.loads(response.read())["entry"]
