from dataclasses import dataclass
from math import radians, sin, cos, asin, sqrt


@dataclass
class Geocoordinates:

    _DEFAULT_KEY_NAMES = {
        "latitude": "lat",
        "longitude": "lng"
    }

    lat: float
    lng: float

    def __post_init__(self):
        errors = list()
        if not -90.0 <= self.lat <= 90.0:
            errors.append(f"lat: {self.lat}")
        if not -180.0 <= self.lng <= 180.0:
            errors.append(f"lng: {self.lng}")
        if len(errors) != 0:
            raise ValueError(f"Invalid value(s) for {self.__class__.__name__}({', '.join(errors)}).")

    def distance_to(self, other) -> float:
        lam_1, lam_2 = radians(self.lng), radians(other.lng)
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (sin((phi_2 - phi_1) / 2)**2 + cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2)**2)
        return 12742 * asin(sqrt(h))

    def to_dict(self, lat="lat", lng="lng") -> dict:
        return {lat: self.lat, lng: self.lng}
