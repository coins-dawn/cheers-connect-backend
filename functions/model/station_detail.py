class StationDetail:
    def __init__(self, id, name, coord_str, kana):
        self.id = id
        self.name = name
        self.lat = float(coord_str.split(",")[0])
        self.lon = float(coord_str.split(",")[1])
        self.coord = coord_str
        self.kana = kana


class StationDetails:
    def __init__(self, station_detail_obj_list: list) -> None:
        self.station_detail_list = [
            StationDetail(elem["id"], elem["name"], elem["coord"], elem["kana"])
            for elem in station_detail_obj_list
        ]
        self.station_detail_dict = {
            station_detail.id: station_detail
            for station_detail in self.station_detail_list
        }

    def is_exist_id(self, target_id: str) -> bool:
        return target_id in self.station_detail_dict

    def search_station_by_id(self, station_id: str) -> StationDetail:
        return self.station_detail_dict[station_id]
