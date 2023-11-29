from dataclasses import dataclass
from model.store_detail import StoreDetail


@dataclass
class GenreCode:
    code: str
    name: str


class GenreCodes:
    def __init__(self, genre_code_obj_list) -> None:
        self.genre_code_list = [
            GenreCode(str(elem["code"]), elem["name"]) for elem in genre_code_obj_list
        ]
        self.name_code_dict = {
            genre_code.name: genre_code.code for genre_code in self.genre_code_list
        }
        self.code_name_dict = {
            genre_code.code: genre_code.name for genre_code in self.genre_code_list
        }
        self.code_set = {genre_code.code for genre_code in self.genre_code_list}

    def is_exist_code(self, target):
        return target in self.code_set

    def intersection(self, store: StoreDetail, genre_code_list: list[int]) -> set:
        store_genre_code_set = {
            self.name_code_dict[genre_name] for genre_name in store.genre_name_list
        }
        return store_genre_code_set & set(genre_code_list)

    def code_to_name(self, code) -> str:
        return self.code_name_dict[code]
