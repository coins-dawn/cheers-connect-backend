from algorithm.gather_station import GatherStation
from model.station_store_distance import StationStoreDistance
from model.store_detail import StoreDetail, StoreDetails
from model.request_parameter import RecommendStoreParameter
from model.store_with_transit import StoreWithTransit

RESPONSE_RECOMMEND_STORE_SIZE = 100  # 返却する店舗の最大個数


class RecommendStore:
    def __init__(
        self,
        store_details: StoreDetails,
        station_store_distance: StationStoreDistance,
        gather_station: GatherStation,
    ) -> None:
        self.store_details = store_details
        self.station_store_distance = station_store_distance
        self.gather_station = gather_station

    @staticmethod
    def filter_by_store_attribute(
        param: RecommendStoreParameter, store_details: StoreDetails
    ) -> list[StoreDetail]:
        filtered_store_list = []
        for store_detail in store_details.store_detail_list:
            if store_detail.dinner_budget_lower_limit > param.budget:
                continue
            if store_detail.comment_num < param.min_comment_num:
                continue
            if store_detail.save_num < param.min_save_num:
                continue
            if store_detail.rate < param.min_rate:
                continue
            if (
                param.free_word != ""
                and param.free_word not in store_detail.description
            ):
                continue
            # TODO: genreについての条件を追加する
            filtered_store_list.append(store_detail)
        return filtered_store_list

    def filtered_by_store_location(
        self, param: RecommendStoreParameter, store_detail_list: list[StoreDetail]
    ) -> list[StoreWithTransit]:
        filtered_store_list = []

        for store_detail in store_detail_list:
            store_with_transit = StoreWithTransit(
                store_detail=store_detail,
                station_store_distance=self.station_store_distance,
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

    def sort(self, store_with_transit_list: StoreWithTransit) -> list[StoreWithTransit]:
        return sorted(
            store_with_transit_list, key=(lambda x: x.store_detail.rate), reverse=True
        )

    def recommend_store(self, param: RecommendStoreParameter) -> list[StoreWithTransit]:
        filtered_by_store_attribute_list = RecommendStore.filter_by_store_attribute(
            param, self.store_details
        )
        filtered_by_location_list = self.filtered_by_store_location(
            param, filtered_by_store_attribute_list
        )
        sorted_store_with_transit_list = self.sort(filtered_by_location_list)
        return sorted_store_with_transit_list[:RESPONSE_RECOMMEND_STORE_SIZE]
