## A simple wrapper for Google's geocoding api. 

Get address data from coordinates or coordinates from an address in one function call. No need to bother with creation of requests and parsing of responses. Distance from a Location to another is available as a method.

```
from gloc import Location

location = Location.from_coordinates(57.696994, 11.986500)

same_location = Location.from_address("Skånegatan 59, 412 52 Göteborg, Sweden")

distance = location.geocoordinates.distance_to(same_location.geocoordinates)
```
Put an api-key in a file named google_api_key.txt in working directory or set environment variable GOOGLE_API_KEY.
