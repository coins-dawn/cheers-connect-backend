from dataclasses import dataclass


@dataclass
class GenreCode:
    code: str
    name: str


class GenreCodes:
    def __init__(self, genre_code_obj_list) -> None:
        self.genre_code_list = [
            GenreCode(str(elem["code"]), elem["name"]) for elem in genre_code_obj_list
        ]
        self.code_name_dict = {
            genre_code.code: genre_code.name for genre_code in self.genre_code_list
        }
        self.code_set = {genre_code.code for genre_code in self.genre_code_list}

    def is_exist_code(self, target):
        return target in self.code_set

    def intersection(self, target_code_set: set):
        return self.code_set & target_code_set

    def code_to_name(self, code):
        return self.code_name_dict[code]
