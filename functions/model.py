class StationDetailList:
    def __init__(self, station_detail_obj_list) -> None:
        self.station_detail_obj_list = station_detail_obj_list
        self.station_detail_dict = {
            station_detail["id"]: station_detail
            for station_detail in station_detail_obj_list
        }

    def is_exist_id(self, target_id: str) -> bool:
        return target_id in self.station_detail_dict


class StoreDetailList:
    def __init__(self, store_detail_obj_list) -> None:
        self.store_detail_obj_list = store_detail_obj_list


class StationStoreDistance:
    def __init__(self, station_store_distance_list) -> None:
        self.station_store_distance_dict = self.__make_station_store_distance_dict(
            station_store_distance_list
        )

    def __make_station_store_distance_dict(self, station_store_distance_list):
        station_store_distance_dict = {}
        for elem in station_store_distance_list:
            station_id = elem["station_id"]
            store_id = elem["store_id"]
            distance = elem["distance_m"]
            if station_id not in station_store_distance_dict:
                station_store_distance_dict[station_id] = {}
            if store_id not in station_store_distance_dict[station_id]:
                station_store_distance_dict[station_id][store_id] = distance
        return station_store_distance_dict

    def get_store_distance_list(self, station_id_str: str) -> dict:
        return self.station_store_distance_dict[station_id_str].items()
