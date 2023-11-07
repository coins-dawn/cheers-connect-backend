import json
from firebase_functions import https_fn
from algorithm.dijkstra import Dijkstra
from algorithm.recommend_store import RecommendStore
from data_accessor.file_accessor import FileAccessor
from data_accessor.db_accessor import DBAccessor
from model.request_parameter import RecommendStoreParameter


def recommend_store(req: https_fn.Request):
    req_param_dict = req.args.to_dict()
    file_accessor = FileAccessor()

    try:
        param = RecommendStoreParameter(req_param_dict, file_accessor.station_details)
    except Exception as e:
        return https_fn.Response(e.__str__(), status=400)

    db_accessor = DBAccessor()
    dijkstra = Dijkstra(
        file_accessor.station_details,
        file_accessor.neighboor_station_dict,
        db_accessor,
    )
    recommend_store = RecommendStore(
        file_accessor.store_detail_list, file_accessor.station_store_distance, dijkstra
    )
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
