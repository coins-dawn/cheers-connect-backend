import json
from firebase_functions import https_fn, options
from firebase_admin import initialize_app
from data_accessor.file_accessor import FileAccessor
from logic.recommend_store import RecommendStore

initialize_app()

MAX_SEARCH_RADIUS_M = 5000  # 駅からの探索半径の最大値[m]


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=[
            r"https://cheers-connect-e3c35.web.app",
            r"http://localhost:3000",
            r"https://cheers-connect-e3c35--.*-.*.web.app",
        ],
        cors_methods=["get", "post"],
    )
)
def execute(req: https_fn.Request) -> https_fn.Response:
    req_param_dict = req.args.to_dict()
    file_accessor = FileAccessor()
    station_detail_list = file_accessor.station_detail_list
    store_detail_list = file_accessor.store_detail_list
    station_store_distance = file_accessor.station_store_distance

    if "station_id" not in req_param_dict:
        return https_fn.Response("error: station_idが指定されていません。", status=400)
    station_id_str = req_param_dict["station_id"]

    if not station_detail_list.is_exist_id(station_id_str):
        return https_fn.Response("error: 存在しないstation_idが指定されています。", status=400)

    if "search_radius" not in req_param_dict:
        return https_fn.Response("error: search_radiusが指定されていません。", status=400)
    search_radius_str = req_param_dict["search_radius"]
    if not search_radius_str.isdecimal():
        return https_fn.Response("error: search_radiusが数値ではありません。", status=400)
    search_radius = int(search_radius_str)
    if search_radius > MAX_SEARCH_RADIUS_M:
        return https_fn.Response(
            f"error: search_radiusが最大値({MAX_SEARCH_RADIUS_M})を超えています。", status=400
        )

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
