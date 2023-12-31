import csv
import json
from model.station_detail import StationDetails
from model.genre_code import GenreCodes
from model.nearest_stations import NearestStations

STATION_DETAIL_FILE = "./static/station_detail_list.json"
NEIGHBOORHOOD_STATION_FILE = "./static/neighborhood_station.json"
GENRE_CODE_FILE = "./static/genre_code.json"
NEAREST_STATION_FILE = "./static/nearest_station.csv"


def read_json_file(file_path, key_str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)[key_str]


def read_csv_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class FileAccessor:
    def __init__(self) -> None:
        station_detail_obj_list = read_json_file(
            STATION_DETAIL_FILE, "station_detail_list"
        )
        self.station_details = StationDetails(station_detail_obj_list)
        self.neighboor_station_dict = read_json_file(
            NEIGHBOORHOOD_STATION_FILE, "station_neighboorhood_dict"
        )
        genre_code_list = read_json_file(GENRE_CODE_FILE, "genre_code_list")
        self.genre_codes = GenreCodes(genre_code_list)
        nearest_station_obj_list = read_csv_file(NEAREST_STATION_FILE)
        self.nearest_stations = NearestStations(nearest_station_obj_list)
