import statistics

from model.store_with_transit import StoreWithTransit
from model.store_with_transit_sort_priority import StoreWithTransitSortPriority


class SortStoreWithTransit:
    @staticmethod
    def store_score(store: StoreWithTransit) -> int:
        # rateから所要時間[min]への変換係数
        rate_to_transittime_coeffecient = 50
        return int((store.store_detail.rate - 3.0) * rate_to_transittime_coeffecient)

    @staticmethod
    def gather_station_score(store: StoreWithTransit) -> int:
        transit_time_list = store.transit_time_to_enter_stations.values()
        mean_transit_time = statistics.mean(transit_time_list)
        max_min_diff = max(transit_time_list) - min(transit_time_list)
        # 所要時間に偏りがある場合は所要時間平均にペナルティを追加
        mean_transit_time_with_fairness = mean_transit_time + (max_min_diff / 2)
        return int(max(60 - mean_transit_time_with_fairness, 0))

    @staticmethod
    def sort(
        store_with_transit_list: list[StoreWithTransit],
        sort_priority: StoreWithTransitSortPriority,
    ) -> list[StoreWithTransit]:
        def sort_key(store: StoreWithTransit) -> float:
            if sort_priority == StoreWithTransitSortPriority.STORE:
                store_score_coefficient = 5.0
                gather_station_score_coefficient = 1.0
            elif sort_priority == StoreWithTransitSortPriority.GATHER_STATION:
                store_score_coefficient = 1.0
                gather_station_score_coefficient = 5.0
            else:
                store_score_coefficient = 1.0
                gather_station_score_coefficient = 1.0
            store_score = SortStoreWithTransit.store_score(store)
            gather_station_score = SortStoreWithTransit.gather_station_score(store)
            return (
                store_score * store_score_coefficient
                + gather_station_score * gather_station_score_coefficient
            )

        return sorted(store_with_transit_list, key=sort_key, reverse=True)
