from geopy.distance import geodesic


class StationDetail:
    def __init__(self, id, name, coord_str, kana):
        self.id = id
        self.name = name
        self.lat = float(coord_str.split(",")[0])
        self.lon = float(coord_str.split(",")[1])
        self.kana = kana
