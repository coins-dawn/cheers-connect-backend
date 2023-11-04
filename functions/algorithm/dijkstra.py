from model.transit import Transit
from model.station_detail import StationDetail
from data_accessor.db_accessor import DBAccessor


class TransitPath:
    def __init__(
        self,
        org_station_id,
        dst_station_id,
        transit_time_sec,
        station_id_sequence,
        is_transfer,
    ):
        self.org_station_id = org_station_id
        self.dst_station_id = dst_station_id
        self.transit_time_sec = transit_time_sec
        self.station_id_sequence = station_id_sequence
        self.is_transfer = is_transfer

    @staticmethod
    def create_expand_begin_target_path(station_id):
        return TransitPath(
            station_id,
            station_id,
            0,
            "",
            False,
        )

    def calc_transfer_time(self):
        """
        乗り換え所要時間を計算する。
        今は固定で10分で返すが、将来的には駅の特性や直通運転も考慮したい。
        """
        if self.is_transfer:
            return 10 * 60  # sec
        # 乗り換えでない場合は0
        return 0

    def to_transit(self) -> Transit:
        return Transit(
            org_station_id=self.org_station_id,
            dst_station_id=self.dst_station_id,
            transit_time_sec=self.transit_time_sec,
            station_id_sequence=self.station_id_sequence,
        )

    def expand(
        self,
        station_neighborhood_dict,
        expand_target_list_dict,
    ):
        if self.is_transfer:
            station_neighboor_set = station_neighborhood_dict[self.dst_station_id]
        else:
            station_neighboor_set = {self.dst_station_id}

        expand_result_list = []
        for station_neighbor_id in station_neighboor_set:
            expand_target_list = expand_target_list_dict[station_neighbor_id]
            for expand_target in expand_target_list:
                commma = "," if self.station_id_sequence != "" else ""
                expand_result_list.append(
                    TransitPath(
                        org_station_id=self.org_station_id,
                        dst_station_id=expand_target.dst_station_id,
                        transit_time_sec=self.transit_time_sec
                        + expand_target.transit_time_sec
                        + self.calc_transfer_time(),
                        station_id_sequence=self.station_id_sequence
                        + commma
                        + expand_target.station_id_sequence,
                        is_transfer=True,
                    )
                )
        return expand_result_list


class Dijkstra:
    transferable_distance_threshold = 200  # [m]

    def __init__(
        self, station_detail_list, neighboorhood_station_dict, db_accessor: DBAccessor
    ) -> None:
        self.station_detail_list = [
            StationDetail(
                id=elem["id"],
                name=elem["name"],
                coord_str=elem["coord"],
                kana=elem["kana"],
            )
            for elem in station_detail_list
        ]
        self.station_neighborhood_dict = neighboorhood_station_dict
        self.expand_target_list_dict = self.calc_expand_target_list_dict(db_accessor)

    def calc_expand_target_list_dict(self, db_accessor: DBAccessor):
        expand_target_list_dict = {}
        for station in self.station_detail_list:
            expand_target_list_dict[
                station.id
            ] = db_accessor.select_transit_record_by_o(station.id)
        return expand_target_list_dict

    def calc_latest_path_to_every_other_stations(self, station_id) -> list[Transit]:
        transit_path = TransitPath.create_expand_begin_target_path(station_id)
        open_path_list_dict = {
            elem.dst_station_id: elem
            for elem in transit_path.expand(
                self.station_neighborhood_dict, self.expand_target_list_dict
            )
        }

        def minimum_cost_transit_path(open_path_list_dict):
            open_path_list = open_path_list_dict.values()
            min_cost = 999999999999
            min_cost_path = None
            for open_path in open_path_list:
                if min_cost > open_path.transit_time_sec:
                    min_cost = open_path.transit_time_sec
                    min_cost_path = open_path
            return min_cost_path

        close_station_id_set = set()
        result_transit_path_list = []
        while len(open_path_list_dict) != 0:
            # 所要時間の最も小さいpathをclose
            min_cost_path = minimum_cost_transit_path(open_path_list_dict)
            del open_path_list_dict[min_cost_path.dst_station_id]
            close_station_id_set.add(min_cost_path.dst_station_id)
            result_transit_path_list.append(min_cost_path)
            # 拡散
            expand_transit_path_list = min_cost_path.expand(
                self.station_neighborhood_dict, self.expand_target_list_dict
            )
            for transit_path in expand_transit_path_list:
                dst_station_id = transit_path.dst_station_id
                if dst_station_id in close_station_id_set:
                    continue
                if dst_station_id in open_path_list_dict:
                    if (
                        open_path_list_dict[dst_station_id].transit_time_sec
                        > transit_path.transit_time_sec
                    ):
                        open_path_list_dict[dst_station_id] = transit_path
                else:
                    open_path_list_dict[dst_station_id] = transit_path
        return [elem.to_transit() for elem in result_transit_path_list]
