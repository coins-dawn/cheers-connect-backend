from model.station_detail import StationDetails


class RecommendStoreParameter:
    MAX_SEARCH_RADIUS_M = 5000  # 駅からの探索半径の最大値[m]
    MAX_BUDGET = 100000  # 予算の最大値[円]
    MAX_TRANSIT_TIME_MINUTE = 600  # 電車での移動時間の最大値[分]

    def __init__(self, req_param_dict: dict, station_details: StationDetails) -> None:
        self.station_details = station_details
        self.station_id_list = self.__get_station_id_list(req_param_dict)
        self.search_radius = self.__get_search_radius(req_param_dict)
        self.genre_code_list = []  # TODO: 実装する
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

    def __get_station_id_list(self, req_param_dict):
        if "station_id" not in req_param_dict:
            raise Exception("error! station_idが指定されていません。")
        station_id_str = req_param_dict["station_id"]
        station_id_list = station_id_str.split("-")
        for station_id in station_id_list:
            if not self.station_details.is_exist_id(station_id):
                raise Exception(f"error! 存在しないstation_id({station_id})が指定されています。")
        return station_id_list

    def __get_search_radius(self, req_param_dict):
        if "search_radius" not in req_param_dict:
            raise Exception("error! search_radiusが指定されていません。")
        search_radius_str = req_param_dict["search_radius"]
        if not search_radius_str.isdecimal():
            raise Exception("error! search_radiusが数値ではありません。")
        search_radius = int(search_radius_str)
        if search_radius > RecommendStoreParameter.MAX_SEARCH_RADIUS_M:
            raise Exception(
                f"error! search_radiusが最大値{RecommendStoreParameter.MAX_SEARCH_RADIUS_M}を超えています。"
            )
        return search_radius

    def __get_optional_num_parameter(self, req_param_dict, param_name, default_value):
        if param_name not in req_param_dict:
            return default_value
        param_str = req_param_dict[param_name]
        if not param_str.isdecimal():
            return Exception(f"error! {param_name}が数値ではありません。")
        return int(param_str)


class SearchRouteParameter:
    def __init__(self) -> None:
        pass
