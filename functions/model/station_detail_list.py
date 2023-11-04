class StationDetailList:
    def __init__(self, station_detail_obj_list) -> None:
        self.station_detail_obj_list = station_detail_obj_list
        self.station_detail_dict = {
            station_detail["id"]: station_detail
            for station_detail in station_detail_obj_list
        }

    def is_exist_id(self, target_id: str) -> bool:
        return target_id in self.station_detail_dict

    def search_station_by_id(self, station_id):
        return self.station_detail_dict[station_id]
