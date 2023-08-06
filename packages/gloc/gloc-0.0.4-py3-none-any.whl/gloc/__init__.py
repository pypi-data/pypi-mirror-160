"""Automates creation of requests to, and parsing of response from Google's geocoding API."""

__version__ = "0.0.4"
__author__ = "Anders Petersson <petersson@chillservices.com>"


import re
import os
from dataclasses import dataclass
from pathlib import Path
import requests

from gloc.geocoordinates import Geocoordinates


def _load_api_key():
    if (path := Path("google_api_key.txt")).exists():
        with open(path, "r", encoding="utf-8") as key_file:
            return key_file.readline()
    if not (key := os.environ.get("GOOGLE_API_KEY")):
        raise IOError("Unable to load api key.")
    return key


def _send(url: str) -> dict:
    return requests.get(url).json()


def _by_address_url(formatted_address: str) -> str:
    url_formatted = re.sub(r",?\s", "%20", formatted_address)
    return f"{_BASE_URL}?address={url_formatted}&key={_GOOGLE_API_KEY}"


def _by_coordinates_url(lat: float, lng: float) -> str:
    return f"{_BASE_URL}?latlng={lat},{lng}&key={_GOOGLE_API_KEY}"


def _parse(response) -> dict:
    if len(response["results"]) == 0:
        return
    best_response = response["results"][0]
    address_components = best_response.get("address_components")
    name_by_types = {tuple(v.get("types")): v.get("long_name") for v in address_components}
    return {
        "street_name": name_by_types.get(("route",)),
        "street_number": name_by_types.get(("street_number",)),
        "zip": name_by_types.get(("postal_code",)),
        "city": name_by_types.get(("locality", "political"), name_by_types.get(("postal_town",))),
        "country": name_by_types.get(("country", "political")),
        "formatted_address": best_response.get("formatted_address"),
        "geocoordinates": Geocoordinates(**best_response["geometry"]["location"])
    }


_GOOGLE_API_KEY = _load_api_key()
_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


@dataclass
class Location:

    street_name: str
    street_number: str
    zip: str
    city: str
    country: str
    formatted_address: str
    geocoordinates: Geocoordinates

    @classmethod
    def from_address(cls, address: str):
        return cls._create(_by_address_url(address))

    @classmethod
    def from_coordinates(cls, lat: float, lng: float):
        return cls._create(_by_coordinates_url(lat, lng))

    @classmethod
    def _create(cls, url: str):
        return cls(**respons) if (respons := _parse(_send(url))) else None

    def distance_to(self, other) -> float:
        return self.geocoordinates.distance_to(other.geocoordinates)
