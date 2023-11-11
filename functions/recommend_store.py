import json
from firebase_functions import https_fn
from algorithm.dijkstra import Dijkstra
from algorithm.gather_station import GatherStation
from algorithm.recommend_store import RecommendStore
from data_accessor.file_accessor import FileAccessor
from data_accessor.db_accessor import DBAccessor
from model.request_parameter import RecommendStoreParameter
from model.store_with_transit import StoreWithTransit
from model.station_detail import StationDetails
from model.genre_code import GenreCodes


def create_response(
    param: RecommendStoreParameter,
    recommend_store_list: list[StoreWithTransit],
    station_details: StationDetails,
    genre_codes: GenreCodes,
) -> https_fn.Response:
    search_conditions = {
        "station_list": [
            {
                "id": station_id,
                "name": station_details.search_station_by_id(station_id).name,
            }
            for station_id in param.station_id_list
        ],
        "nearest_station_distance_limit": param.nearest_station_distance_limit,
        "genre_code_list": [
            {"code": genre_code, "name": genre_codes.code_to_name(genre_code)}
            for genre_code in param.genre_code_list
        ],
        "budget": param.budget,
        "min_comment_num": param.min_comment_num,
        "min_save_num": param.min_save_num,
        "max_transit_time_minute": param.max_transit_time_minute,
        "free_word": param.free_word,
        "min_rate": param.min_rate,
    }
    search_result = [
        {
            "store_detail": elem.store_detail.__dict__(),
            "transit_time": elem.transit_time_to_enter_stations,
            "nearest_station": {
                "id": elem.nearest_station_id,
                "name": station_details.search_station_by_id(
                    elem.nearest_station_id
                ).name,
                "distance_m": elem.nearest_station_distance_m,
            },
        }
        for elem in recommend_store_list
    ]
    return https_fn.Response(
        json.dumps(
            {"search_conditions": search_conditions, "search_result": search_result},
            ensure_ascii=False,
            indent=2,
        ),
        status=200,
    )


def recommend_store(req: https_fn.Request) -> https_fn.Response:
    req_param_dict = req.args.to_dict()
    file_accessor = FileAccessor()

    try:
        param = RecommendStoreParameter(
            req_param_dict, file_accessor.station_details, file_accessor.genre_codes
        )
    except Exception as e:
        return https_fn.Response(e.__str__(), status=400)

    db_accessor = DBAccessor()
    dijkstra = Dijkstra(
        file_accessor.station_details,
        file_accessor.neighboor_station_dict,
        db_accessor,
    )
    gather_station = GatherStation(param.station_id_list, dijkstra)
    recommend_store = RecommendStore(
        file_accessor.store_details,
        file_accessor.nearest_stations,
        gather_station,
        file_accessor.genre_codes,
    )
    recommend_store_list = recommend_store.recommend_store(param)

    return create_response(
        param,
        recommend_store_list,
        file_accessor.station_details,
        file_accessor.genre_codes,
    )
