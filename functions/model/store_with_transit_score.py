import statistics
from model.store_with_transit_sort_priority import StoreWithTransitSortPriority


class StoreWithTransitScore:
    # rateから所要時間[min]への変換係数
    STORE_RATE_TO_TRANSITTIME_COEFFICIENT = 50

    def __init__(
        self,
        store_rate: float,
        transit_time_list: list[int],
    ) -> None:
        self.store_score = StoreWithTransitScore.calc_store_score(store_rate)
        self.gather_station_score = StoreWithTransitScore.calc_gather_station_score(
            transit_time_list
        )

    @classmethod
    def calc_store_score(cls, store_rate: float) -> int:
        rate_to_transittime_coeffecient = 50
        return int((store_rate - 3.0) * rate_to_transittime_coeffecient)

    @staticmethod
    def calc_gather_station_score(transit_time_list: list[int]) -> int:
        worst_gather_station_score = -9999999
        if len(transit_time_list) == 0:
            return worst_gather_station_score

        mean_transit_time = statistics.mean(transit_time_list)
        max_min_diff = max(transit_time_list) - min(transit_time_list)
        # 所要時間に偏りがある場合は所要時間平均にペナルティを追加
        mean_transit_time_with_fairness = mean_transit_time + (max_min_diff / 2)
        return int(-mean_transit_time_with_fairness)

    @staticmethod
    def get_score_coefficients(
        priority: StoreWithTransitSortPriority,
    ) -> tuple[int, int]:
        if priority == StoreWithTransitSortPriority.STORE:
            store_score_coefficient = 5.0
            gather_station_score_coefficient = 1.0
        elif priority == StoreWithTransitSortPriority.GATHER_STATION:
            store_score_coefficient = 1.0
            gather_station_score_coefficient = 5.0
        else:
            store_score_coefficient = 1.0
            gather_station_score_coefficient = 1.0
        return store_score_coefficient, gather_station_score_coefficient

    def get_score(self, priority: StoreWithTransitSortPriority) -> int:
        (
            store_score_coefficient,
            gather_station_score_coefficient,
        ) = StoreWithTransitScore.get_score_coefficients(priority)
        return (
            self.store_score * store_score_coefficient
            + self.gather_station_score * gather_station_score_coefficient
        )

    def __dict__(self, priority: StoreWithTransitSortPriority):
        (
            store_score_coefficient,
            gather_station_score_coefficient,
        ) = StoreWithTransitScore.get_score_coefficients(priority)
        return {
            "total_score": self.get_score(priority),
            "store": {
                "score * coefficient": self.store_score * store_score_coefficient,
                "score": self.store_score,
                "coefficient": store_score_coefficient,
            },
            "gather_station": {
                "score * coefficient": self.gather_station_score
                * gather_station_score_coefficient,
                "score": self.gather_station_score,
                "coefficient": gather_station_score_coefficient,
            },
        }
