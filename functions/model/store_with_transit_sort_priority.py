from enum import Enum


class StoreWithTransitSortPriority(Enum):
    """
    StoreWithTransitをソートする際に何を重視するか
    """

    # バランス
    BALANCE = 0
    # 集合駅の良さ
    GATHER_STATION = 1
    # 店舗の良さ
    STORE = 2

    @staticmethod
    def str_to_enum_dict():
        return {
            "balance": StoreWithTransitSortPriority.BALANCE,
            "gather_station": StoreWithTransitSortPriority.GATHER_STATION,
            "store": StoreWithTransitSortPriority.STORE,
        }

    @staticmethod
    def valid_key_list() -> list[str]:
        return StoreWithTransitSortPriority.str_to_enum_dict().keys()

    @staticmethod
    def is_valid_key(target_str: str) -> bool:
        return target_str in StoreWithTransitSortPriority.valid_key_list()

    @staticmethod
    def convert_from_str(target_str: str):
        if not StoreWithTransitSortPriority.is_valid_key(target_str):
            raise Exception("無効な文字列が指定されています。")
        return StoreWithTransitSortPriority.str_to_enum_dict()[target_str]
