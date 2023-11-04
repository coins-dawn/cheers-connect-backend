import json
from firebase_functions import https_fn
from data_accessor.file_accessor import FileAccessor
from data_accessor.db_accessor import DBAccessor
from algorithm.dijkstra import Dijkstra
from model.transit import Transit
from model.station_detail_list import StationDetailList


def check_station_id(req_param_dict, param_name, station_detail_list):
    if param_name not in req_param_dict:
        return False, f"error: {param_name}が指定されていません。"

    station_id = req_param_dict[param_name]
    if not station_detail_list.is_exist_id(station_id):
        return False, f"error: 存在しない{param_name}が指定されています。"

    return True, ""


def check_request_param(req_param_dict, station_detail_list):
    is_valid_params, message = check_station_id(
        req_param_dict, "org_station_id", station_detail_list
    )
    if not is_valid_params:
        return False, message

    is_valid_params, message = check_station_id(
        req_param_dict, "dst_station_id", station_detail_list
    )
    if not is_valid_params:
        return False, message

    return True, ""


def transit_to_response_obj(transit: Transit, station_detail_list: StationDetailList):
    station_id_list = transit.station_id_sequence.split(",")
    org_station_obj = station_detail_list.search_station_by_id(transit.org_station_id)
    dst_station_obj = station_detail_list.search_station_by_id(transit.dst_station_id)
    station_list = []
    for station_id in station_id_list:
        station_obj = station_detail_list.search_station_by_id(station_id)
        station_list.append(
            {
                "id": station_id,
                "name": station_obj["name"],
                "coord": station_obj["coord"],
            }
        )
    return {
        "org_station": {"id": transit.org_station_id, "name": org_station_obj["name"]},
        "dst_station": {"id": transit.dst_station_id, "name": dst_station_obj["name"]},
        "transit_time_minute": int(transit.transit_time_sec / 60),
        "station_list": station_list,
    }


def search_route(req):
    req_param_dict = req.args.to_dict()
    file_accessor = FileAccessor()
    station_detail_list = file_accessor.station_detail_list
    neighboorhood_station_dict = file_accessor.neighboor_station_dict
    db_accessor = DBAccessor()

    is_valid_params, message = check_request_param(req_param_dict, station_detail_list)
    if not is_valid_params:
        return https_fn.Response(message, status=400)

    org_station_id = req_param_dict["org_station_id"]
    dst_station_id = req_param_dict["dst_station_id"]

    dijkstra = Dijkstra(
        station_detail_list.station_detail_obj_list,
        neighboorhood_station_dict,
        db_accessor,
    )
    org_to_every_station_transit_list = (
        dijkstra.calc_latest_path_to_every_other_stations(org_station_id)
    )
    target_transit_obj = None
    for transit in org_to_every_station_transit_list:
        if transit.dst_station_id == dst_station_id:
            target_transit_obj = transit
            break
    else:
        return https_fn.Response("error! 経路が見つかりませんでした。", status=400)

    return https_fn.Response(
        json.dumps(
            transit_to_response_obj(target_transit_obj, station_detail_list),
            ensure_ascii=False,
            indent=2,
        ),
        status=200,
    )
