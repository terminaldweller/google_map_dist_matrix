#!/usr/bin/env python

import argparse
import csv
import concurrent.futures
import functools
import os
import sys
import typing

import googlemaps
import requests


class Argparser:  # pylint: disable=too-few-public-methods
    """Argparser class."""

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--csv", type=str, help="path to the csv file", default="")
        parser.add_argument(
            "--maxworkers",
            type=int,
            help="maxworkers to pass to ThreadPoolExecutor",
            default=32,
        )
        parser.add_argument(
            "--apikey", type=str, help="google maps api key", default=""
        )
        self.args = parser.parse_args()


def single_get_tag(gmaps, args) -> typing.Tuple[int, int]:
    try:
        result = gmaps.distance_matrix(args[0], args[1], mode="driving")["rows"][0][
            "elements"
        ][0]["distance"]["value"]
    except:
        result = 0
    return result, args[2]


def multi_get_tag(
    max_workers: int, gmaps, args: typing.List[typing.Tuple[str, str, int]]
) -> typing.List[typing.Tuple[int, int]]:
    func = functools.partial(single_get_tag, gmaps)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(func, args))
    return results


def get_address_pairs_csv(
    path: str,
) -> typing.Tuple[typing.List[str], typing.List[str]]:
    a: typing.List[str] = []
    b: typing.List[str] = []

    with open(path, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            a.append(row["\ufeffA"])
            b.append(row["B"])

    return a, b


def main() -> None:
    results: typing.List[int] = []
    argparser = Argparser()
    csv_file = argparser.args.csv
    if csv_file == "":
        print("did not provide path to a csv file. exiting ...")
        sys.exit(1)

    api_key = argparser.args.apikey
    if api_key == "":
        api_key = os.environ["GOOGLE_MAPS_API_KEY"]
    gmaps = googlemaps.Client(key=api_key)

    a, b = get_address_pairs_csv(csv_file)

    iterable = list(zip(a, b, list(range(1, len(a)))))
    max_workers = argparser.args.maxworkers
    result = multi_get_tag(max_workers, gmaps, iterable)
    print(result)


if __name__ == "__main__":
    main()
