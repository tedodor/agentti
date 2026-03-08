#!/usr/bin/env python3

import requests
import argparse
import os

url = "https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}"

parser = argparse.ArgumentParser()
parser.add_argument('lat')
parser.add_argument('lon')

args = parser.parse_args()

def run(lat, lon, key):
    s = requests.get(
        url.format(
            lat=lat, lon=lon, key=key
        )
    )
    if s.status_code == 200:
        return s.content
    return "API key error"

if __name__ == '__main__':
    api_key = os.environ['OPEN_WEATHER_API_KEY']

    print(
        run(args.lat, args.lon, api_key)
    )