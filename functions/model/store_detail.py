class StoreDetail:
    def __init__(
        self,
        id: int,
        store_name: str,
        genre_str: str,
        description: str,
        area: str,
        rate: float,
        coord: str,
        comment_num: int,
        save_num: int,
        dinner_budget_upper_limit: int,
        dinner_budget_lower_limit: int,
        url: str,
    ) -> None:
        self.id = id
        self.name = store_name
        self.genre_name_list = genre_str.split("、")
        self.description = description
        self.area = area
        self.rate = rate
        self.coord = coord
        self.comment_num = comment_num
        self.save_num = save_num
        self.dinner_budget_upper_limit = dinner_budget_upper_limit
        self.dinner_budget_lower_limit = dinner_budget_lower_limit
        self.url = url

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "genre": self.genre_name_list,
            "description": self.description,
            "area": self.area,
            "rate": self.rate,
            "coord": self.coord,
            "comment_num": self.comment_num,
            "save_num": self.save_num,
            "dinner_budget_lower_limit": self.dinner_budget_lower_limit,
            "dinner_budget_upper_limit": self.dinner_budget_upper_limit,
            "url": self.url,
        }
