class NearestStations:
    def __init__(self, nearest_station_obj_list) -> None:
        self.storeid_nearest_stationdict = {
            elem["store_id"]: (elem["nearest_station_id"], int(elem["distance"]))
            for elem in nearest_station_obj_list
        }

    def get_nearest_station_by_store_id(self, store_id) -> tuple:
        nearest_station_id, distance = self.storeid_nearest_stationdict[store_id]
        return nearest_station_id, distance
