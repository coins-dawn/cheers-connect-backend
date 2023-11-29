from model.station_detail import StationDetails
from model.genre_code import GenreCodes
from model.store_with_transit_sort_priority import StoreWithTransitSortPriority


class RecommendStoreParameter:
    MAX_SEARCH_RADIUS_M = 5000  # 駅からの店舗の直線距離の最大値[m]
    MAX_BUDGET = 1000000  # 予算の最大値[円]
    MAX_TRANSIT_TIME_MINUTE = 600  # 電車での移動時間の最大値[分]

    def __init__(
        self,
        req_param_dict: dict,
        station_details: StationDetails,
        genre_codes: GenreCodes,
    ) -> None:
        self.station_id_list = self.__get_station_id_list(
            req_param_dict, station_details
        )
        self.nearest_station_distance_limit = self.__get_optional_num_parameter(
            req_param_dict,
            "nearest_station_distance_limit",
            RecommendStoreParameter.MAX_SEARCH_RADIUS_M,
        )
        self.genre_code_list = self.__get_genre_code_list(req_param_dict, genre_codes)
        self.budget = self.__get_optional_num_parameter(
            req_param_dict, "budget", RecommendStoreParameter.MAX_BUDGET
        )
        self.min_comment_num = self.__get_optional_num_parameter(
            req_param_dict, "min_comment_num", 0
        )
        self.min_save_num = self.__get_optional_num_parameter(
            req_param_dict, "min_save_num", 0
        )
        self.max_transit_time_minute = self.__get_optional_num_parameter(
            req_param_dict,
            "max_transit_time_minute",
            RecommendStoreParameter.MAX_TRANSIT_TIME_MINUTE,
        )
        self.free_word = (
            req_param_dict["free_word"] if "free_word" in req_param_dict else ""
        )
        self.min_rate = (
            float(req_param_dict["min_rate"])
            if "min_rate" in req_param_dict and req_param_dict["min_rate"] != "-"
            else 0.0
        )
        self.store_sort_priority = self.__get_store_sort_priority(req_param_dict)

    def __get_station_id_list(self, req_param_dict, station_details: StationDetails):
        if "station_id" not in req_param_dict:
            raise Exception("error! station_idが指定されていません。")
        station_id_str = req_param_dict["station_id"]
        station_id_list = station_id_str.split("-")
        for station_id in station_id_list:
            if not station_details.is_exist_id(station_id):
                raise Exception(f"error! 存在しないstation_id({station_id})が指定されています。")
        return station_id_list

    def __get_genre_code_list(self, req_param_dict, genre_codes: GenreCodes):
        if "genre_code" not in req_param_dict:
            return []
        genre_code_list = req_param_dict["genre_code"].split("-")
        for genre_code in genre_code_list:
            if not genre_codes.is_exist_code(genre_code):
                raise Exception(f"error! 存在しないgenre_code({genre_code})が指定されています。")
        return genre_code_list

    def __get_optional_num_parameter(self, req_param_dict, param_name, default_value):
        if param_name not in req_param_dict:
            return default_value
        param_str = req_param_dict[param_name]
        if not param_str.isdecimal():
            return Exception(f"error! {param_name}が数値ではありません。")
        return int(param_str)

    def __get_store_sort_priority(self, req_param_dict):
        param_name = "store_sort_priority"
        if param_name not in req_param_dict:
            return StoreWithTransitSortPriority.BALANCE
        param_str = req_param_dict[param_name]
        if not StoreWithTransitSortPriority.is_valid_key(param_str):
            valid_param_str = ",".join(StoreWithTransitSortPriority.valid_key_list())
            raise Exception(
                f"error! {param_name}が無効な値です。次のいずれかを指定してください：{valid_param_str}"
            )
        return StoreWithTransitSortPriority.convert_from_str(param_str)


class SearchRouteParameter:
    def __init__(self) -> None:
        pass
