import json
from firebase_functions import https_fn
from data_accessor.file_accessor import FileAccessor
from model.station_store_distance import StationStoreDistance
from model.store_detail_list import StoreDetailList
from model.request_parameter import RecommendStoreParameter


class RecommendStore:
    def __init__(
        self,
        store_detail_list: StoreDetailList,
        station_store_distance: StationStoreDistance,
    ) -> None:
        self.store_detail_list = store_detail_list
        self.station_store_distance = station_store_distance

    def recommend_store(self, param: RecommendStoreParameter) -> dict:
        store_distance_list = self.station_store_distance.get_store_distance_list(
            param.station_id_list[0]
        )
        distance_filtered_store_distance_list = list(
            filter(lambda x: int(x[1]) <= param.search_radius, store_distance_list)
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


def recommend_store(req: https_fn.Request):
    req_param_dict = req.args.to_dict()

    file_accessor = FileAccessor()
    station_detail_list = file_accessor.station_detail_list
    store_detail_list = file_accessor.store_detail_list
    station_store_distance = file_accessor.station_store_distance

    try:
        param = RecommendStoreParameter(req_param_dict, station_detail_list)
    except Exception as e:
        return https_fn.Response(e.__str__(), status=400)

    recommend_store = RecommendStore(store_detail_list, station_store_distance)
    recommend_store_list = recommend_store.recommend_store(param)

    return https_fn.Response(
        json.dumps(
            {
                "request_param": req_param_dict,
                "recommend_store_list": recommend_store_list,
            },
            ensure_ascii=False,
            indent=2,
        ),
        status=200,
    )
