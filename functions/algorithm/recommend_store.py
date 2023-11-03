from model.station_store_distance import StationStoreDistance
from model.store_detail_list import StoreDetailList


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
