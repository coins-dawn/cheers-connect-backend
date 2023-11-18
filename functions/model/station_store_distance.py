class StationStoreDistance:
    def __init__(self, station_store_distance_list) -> None:
        # station_id -> store_id -> distance_m
        self.station_store_distance_dict = self.__make_station_store_distance_dict(
            station_store_distance_list
        )

    def __make_station_store_distance_dict(self, station_store_distance_list):
        station_store_distance_dict = {}
        for elem in station_store_distance_list:
            station_id = elem["station_id"]
            store_id = elem["store_id"]
            distance = int(elem["distance_m"])
            if station_id not in station_store_distance_dict:
                station_store_distance_dict[station_id] = {}
            if store_id not in station_store_distance_dict[station_id]:
                station_store_distance_dict[station_id][store_id] = distance
        return station_store_distance_dict

    def get_store_distance_list(self, station_id_str: str) -> dict:
        return self.station_store_distance_dict[station_id_str].items()
