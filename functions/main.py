from firebase_functions import https_fn, options
from firebase_admin import initialize_app
import json
import csv
from model import StationDetailList, StoreDetailList, StationStoreDistance

initialize_app()

MAX_SEARCH_RADIUS_M = 5000  # 駅からの探索半径の最大値[m]


def read_json_file(file_path, key_str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)[key_str]


def read_csv_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def road_data() -> tuple:
    station_detail_obj_list = read_json_file(
        "./static/station_detail_list.json", "station_detail_list"
    )
    station_detail_list = StationDetailList(station_detail_obj_list)
    store_detail_obj_list = read_json_file(
        "./static/store_detail_list.json", "store_detail_list"
    )
    store_detail_list = StoreDetailList(store_detail_obj_list)
    station_store_distance_obj_list = read_csv_file(
        "./static/station_store_distance.csv"
    )
    station_store_distance = StationStoreDistance(station_store_distance_obj_list)
    return station_detail_list, store_detail_list, station_store_distance


def recommend_store_by_station(
    station_id_str: str,
    search_radius: int,
    store_detail_list: StoreDetailList,
    station_store_distance: StationStoreDistance,
) -> dict:
    store_distance_list = station_store_distance.get_store_distance_list(station_id_str)
    distance_filtered_store_distance_list = list(
        filter(lambda x: int(x[1]) <= search_radius, store_distance_list)
    )
    distance_filtered_store_id_set = {
        elem[0] for elem in distance_filtered_store_distance_list
    }
    represent_drink_enable_store_list = []
    for elem in store_detail_list.store_detail_obj_list:
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
    station_detail_list, store_detail_list, station_store_distance = road_data()

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

    recommend_store_list = recommend_store_by_station(
        station_id_str, search_radius, store_detail_list, station_store_distance
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
