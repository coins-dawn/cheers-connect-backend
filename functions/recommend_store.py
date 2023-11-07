import json
from firebase_functions import https_fn
from data_accessor.file_accessor import FileAccessor
from model.station_store_distance import StationStoreDistance
from model.store_detail_list import StoreDetailList


MAX_SEARCH_RADIUS_M = 5000  # 駅からの探索半径の最大値[m]


class RecommendStore:
    def __init__(
        self,
        store_detail_list: StoreDetailList,
        station_store_distance: StationStoreDistance,
    ) -> None:
        self.store_detail_list = store_detail_list
        self.station_store_distance = station_store_distance

    def recommend_store_by_station(
        self,
        station_id_str: str,
        search_radius: int,
    ) -> dict:
        store_distance_list = self.station_store_distance.get_store_distance_list(
            station_id_str
        )
        distance_filtered_store_distance_list = list(
            filter(lambda x: int(x[1]) <= search_radius, store_distance_list)
        )
        distance_filtered_store_id_set = {
            elem[0] for elem in distance_filtered_store_distance_list
        }
        represent_drink_enable_store_list = []
        for elem in self.store_detail_list.store_detail_obj_list:
            if str(elem["id"]) not in distance_filtered_store_id_set:
                continue
            if not elem.get("represent_drink"):
                continue
            price_str = elem["represent_drink"]["price"].replace("円", "")
            if not price_str.isdecimal():
                continue
            price = int(price_str)
            represent_drink_enable_store_list.append((price, elem))

        sorted_store_distance_list = sorted(
            represent_drink_enable_store_list, key=lambda x: x[0]
        )
        return [elem[1] for elem in sorted_store_distance_list[:10]]


def check_request_params(req_param_dict, station_detail_list):
    if "station_id" not in req_param_dict:
        return False, "error: station_idが指定されていません。"

    station_id_str = req_param_dict["station_id"]
    if not station_detail_list.is_exist_id(station_id_str):
        return False, "error: 存在しないstation_idが指定されています。"

    if "search_radius" not in req_param_dict:
        return False, "error: search_radiusが指定されていません。"

    search_radius_str = req_param_dict["search_radius"]
    if not search_radius_str.isdecimal():
        return False, "error: search_radiusが数値ではありません。"

    search_radius = int(search_radius_str)
    if search_radius > MAX_SEARCH_RADIUS_M:
        return False, f"error: search_radiusが最大値({MAX_SEARCH_RADIUS_M})を超えています。"

    return True, ""


def recommend_store(req: https_fn.Request):
    req_param_dict = req.args.to_dict()
    file_accessor = FileAccessor()
    station_detail_list = file_accessor.station_detail_list
    store_detail_list = file_accessor.store_detail_list
    station_store_distance = file_accessor.station_store_distance

    is_valid_params, message = check_request_params(req_param_dict, station_detail_list)
    if not is_valid_params:
        return https_fn.Response(message, status=400)

    station_id_str = req_param_dict["station_id"]
    search_radius = int(req_param_dict["search_radius"])
    recommend_store = RecommendStore(store_detail_list, station_store_distance)
    recommend_store_list = recommend_store.recommend_store_by_station(
        station_id_str, search_radius
    )
    station_info = station_detail_list.station_detail_dict[station_id_str]

    return https_fn.Response(
        json.dumps(
            {
                "station_info": station_info,
                "search_radius": search_radius,
                "recommend_store_list": recommend_store_list,
            },
            ensure_ascii=False,
            indent=2,
        ),
        status=200,
    )
