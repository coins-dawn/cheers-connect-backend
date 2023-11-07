from algorithm.dijkstra import Dijkstra


class GatherStation:
    def __init__(self, station_id_list: list[str], dijkstra: Dijkstra) -> None:
        # 各駅 -> 乗る駅 -> 所要時間 のdict
        # 乗る駅のいずれかから到達不可能な駅は削除されている
        self.transit_dict = self.__calc_transit_dict(station_id_list, dijkstra)

    @staticmethod
    def __calc_transit_dict(station_id_list: list[str], dijkstra: Dijkstra):
        transit_dict = {}
        for station_id in station_id_list:
            org_to_every_station_transit_list = (
                dijkstra.calc_latest_path_to_every_other_stations(station_id)
            )
            for transit in org_to_every_station_transit_list:
                org_station_id = transit.org_station_id
                dst_station_id = transit.dst_station_id
                if dst_station_id in transit_dict:
                    transit_dict[dst_station_id][
                        org_station_id
                    ] = transit.transit_time_sec
                else:
                    transit_dict[dst_station_id][org_station_id] = {
                        org_station_id: transit.transit_time_sec
                    }
        # 乗る駅のいずれかから到達不可能な駅は削除
        return {
            key: value
            for key, value in transit_dict.items()
            if len(value) == len(station_id_list)
        }
