#!/usr/bin/env python

import argparse
import csv
import os
import typing

import googlemaps
import requests


class Argparser:  # pylint: disable=too-few-public-methods
    """Argparser class."""

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--csv", type=str, help="path to the csv file", default="")
        parser.add_argument(
            "--apikey", type=str, help="google maps api key", default=""
        )
        self.args = parser.parse_args()


def get_address_pairs_csv(path: str) -> typing.List[typing.List[str]]:
    address_pairs: typing.List[typing.List[str]] = []

    with open(path, "r") as file:
        reader = csv.reader(file)
        return list(reader)


def main():
    argparser = Argparser()
    csv_file = argparser.args.csv
    if csv_file == "":
        print("did not provide path to a csv file. exiting ...")
        return 1

    api_key = argparser.args.apikey
    if api_key == "":
        api_key = os.environ["GOOGLE_MAPS_API_KEY"]
    gmaps = googlemaps.Client(key=api_key)
    service = googlemaps.distance_matrix()

    address_pairs = get_address_pairs_csv(csv_file)
    print(address_pairs)


if __name__ == "__main__":
    main()
