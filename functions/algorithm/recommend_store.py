from algorithm.gather_station import GatherStation
from algorithm.sort_store_with_transit import SortStoreWithTransit
from model.store_detail import StoreDetail
from model.request_parameter import RecommendStoreParameter
from model.store_with_transit import StoreWithTransit
from model.genre_code import GenreCodes
from model.nearest_stations import NearestStations
from model.store_with_transit_sort_priority import StoreWithTransitSortPriority
from data_accessor.store_db_accessor import StoreDetailDBAccessor

RESPONSE_RECOMMEND_STORE_SIZE = 100  # 返却する店舗の最大個数


class RecommendStore:
    def __init__(
        self,
        store_db_accessor: StoreDetailDBAccessor,
        nearest_stations: NearestStations,
        gather_station: GatherStation,
        genre_codes: GenreCodes,
    ) -> None:
        self.store_db_accessor = store_db_accessor
        self.nearest_stations = nearest_stations
        self.gather_station = gather_station
        self.genre_codes = genre_codes

    def filter_by_store_attribute(
        self,
        param: RecommendStoreParameter,
    ) -> list[StoreDetail]:
        base_store_list = self.store_db_accessor.filter_by_store_attributes(
            budget=param.budget,
            min_comment_num=param.min_comment_num,
            min_save_num=param.min_save_num,
            min_rate=param.min_rate,
        )
        filtered_store_list = []
        for store_detail in base_store_list:
            if (
                param.free_word != ""
                and param.free_word not in store_detail.description
            ):
                continue
            if param.genre_code_list:
                if not self.genre_codes.intersection(
                    store_detail, param.genre_code_list
                ):
                    continue
            filtered_store_list.append(store_detail)
        return filtered_store_list

    def filtered_by_store_location(
        self, param: RecommendStoreParameter, store_detail_list: list[StoreDetail]
    ) -> list[StoreWithTransit]:
        filtered_store_list = []

        for store_detail in store_detail_list:
            store_with_transit = StoreWithTransit(
                store_detail=store_detail,
                nearest_stations=self.nearest_stations,
                gather_station=self.gather_station,
            )
            if store_with_transit.is_invalid():
                continue
            if (
                store_with_transit.nearest_station_distance_m
                > param.nearest_station_distance_limit
            ):
                continue
            if store_with_transit.max_transit_time() > param.max_transit_time_minute:
                continue
            filtered_store_list.append(store_with_transit)
        return filtered_store_list

    def sort(
        self,
        store_with_transit_list: StoreWithTransit,
        sort_priority: StoreWithTransitSortPriority,
    ) -> list[StoreWithTransit]:
        return SortStoreWithTransit.sort(store_with_transit_list, sort_priority)

    def recommend_store(self, param: RecommendStoreParameter) -> list[StoreWithTransit]:
        filtered_by_store_attribute_list = self.filter_by_store_attribute(
            param,
        )
        filtered_by_location_list = self.filtered_by_store_location(
            param, filtered_by_store_attribute_list
        )
        sorted_store_with_transit_list = self.sort(
            filtered_by_location_list, param.store_sort_priority
        )
        return sorted_store_with_transit_list[:RESPONSE_RECOMMEND_STORE_SIZE]
