from algorithm.gather_station import GatherStation
from model.store_detail import StoreDetail
from model.station_store_distance import StationStoreDistance


class StoreWithTransit:
    def __init__(
        self,
        store_detail: StoreDetail,
        station_store_distance: StationStoreDistance,
        gather_station: GatherStation,
    ) -> None:
        self.store_detail = store_detail
        (
            self.nearest_station_id,
            self.nearest_station_distance_m,
        ) = self.__calc_nearest_station(station_store_distance)
        self.transit_time_to_enter_stations = gather_station.transit_dict.get(
            self.nearest_station_id
        )

    def is_invalid(self):
        return self.transit_time_to_enter_stations == None

    def __calc_nearest_station(self, station_store_distance: StationStoreDistance):
        """
        店舗の最寄り駅、および最寄り駅までの距離を計算する。
        """
        # TODO: 最寄り駅は事前計算したい
        nearest_station_id = -1
        nearest_station_distance_m = 999999999999999
        for (
            station_id,
            store_distance_dict,
        ) in station_store_distance.station_store_distance_dict.items():
            for store_id, distance_m in store_distance_dict.items():
                if self.store_detail.id != store_id:
                    continue
                if nearest_station_distance_m > distance_m:
                    nearest_station_id = station_id
                    nearest_station_distance_m = distance_m
        return nearest_station_id, nearest_station_distance_m

    def max_transit_time(self) -> int:
        return max(self.transit_time_to_enter_stations.values())
