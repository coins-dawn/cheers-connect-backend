from algorithm.gather_station import GatherStation
from model.store_detail import StoreDetail
from model.nearest_stations import NearestStations


class StoreWithTransit:
    def __init__(
        self,
        store_detail: StoreDetail,
        nearest_stations: NearestStations,
        gather_station: GatherStation,
    ) -> None:
        self.store_detail = store_detail
        (
            self.nearest_station_id,
            self.nearest_station_distance_m,
        ) = nearest_stations.get_nearest_station_by_store_id(store_detail.id)
        self.transit_time_to_enter_stations = gather_station.transit_dict.get(
            self.nearest_station_id
        )

    def is_invalid(self):
        return self.transit_time_to_enter_stations == None

    def max_transit_time(self) -> int:
        return max(self.transit_time_to_enter_stations.values())
