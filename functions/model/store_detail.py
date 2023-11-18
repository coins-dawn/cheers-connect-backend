class Drink:
    def __init__(
        self, name: str, price_str: str, extra_info: str, genre_name: str
    ) -> None:
        self.name = name
        self.price = price_str.strip("円")
        self.extra_info = extra_info
        self.genre_name = genre_name

    def __dict__(self):
        return {
            "name": self.name,
            "price": self.price,
            "extra_info": self.extra_info,
            "genre_name": self.genre_name,
        }


class StoreDetail:
    def __init__(
        self,
        id: str,
        store_name: str,
        genre_str: str,
        description: str,
        area: str,
        rate_str: str,
        coord: str,
        comment_num: str,
        save_num_str: str,
        dinner_budget_str: str,
        lunch_budget_str: str,
        url: str,
        drink: Drink,
    ) -> None:
        self.id = id
        self.name = store_name
        self.genre = genre_str
        self.description = description
        self.area = area
        self.rate = float(rate_str) if rate_str and rate_str != "-" else 0
        self.coord = coord
        self.comment_num = int(comment_num) if comment_num else 0
        self.save_num = int(save_num_str) if save_num_str else 0

        def calc_budget_upper_and_lower_limit(budget_str):
            if not budget_str:
                return "", ""
            lower_limit_str, upper_limit_str = budget_str.replace("￥", "").split("～")
            return int(lower_limit_str), int(upper_limit_str)

        (
            dinner_budget_lower_limit,
            dinner_budget_upper_limit,
        ) = calc_budget_upper_and_lower_limit(dinner_budget_str)
        (
            lunch_budget_lower_limit,
            lunch_budget_upper_limit,
        ) = calc_budget_upper_and_lower_limit(lunch_budget_str)
        self.dinner_budget_lower_limit = dinner_budget_lower_limit
        self.dinner_budget_upper_limit = dinner_budget_upper_limit
        self.lunch_budget_lower_limit = lunch_budget_lower_limit
        self.lunch_budget_upper_limit = lunch_budget_upper_limit
        self.url = url
        self.represent_drink = drink

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "genre": self.genre,
            "description": self.description,
            "area": self.area,
            "rate": self.rate,
            "coord": self.coord,
            "comment_num": self.comment_num,
            "save_num": self.save_num,
            "dinner_budget_lower_limit": self.dinner_budget_lower_limit,
            "dinner_budget_upper_limit": self.dinner_budget_upper_limit,
            "lunch_budget_lower_limit": self.lunch_budget_lower_limit,
            "lunch_budget_upper_limit": self.lunch_budget_upper_limit,
            "url": self.url,
            "represent_drink": self.represent_drink.__dict__(),
        }


class StoreDetails:
    def __init__(self, store_detail_obj_list: list) -> None:
        self.store_detail_list = StoreDetails.__make_store_detail_list(
            store_detail_obj_list
        )

    @staticmethod
    def __make_store_detail_list(store_detail_obj_list: list) -> list[StoreDetail]:
        store_detail_list = []
        for elem in store_detail_obj_list:
            represent_drink = None
            if not elem["represent_drink"]:
                continue
            represent_drink = Drink(
                name=elem["represent_drink"]["drink_name"],
                price_str=elem["represent_drink"]["price"],
                extra_info=elem["represent_drink"]["extra_info"],
                genre_name=elem["represent_drink"]["genre_name"],
            )
            store_detail_list.append(
                StoreDetail(
                    id=str(elem["id"]),
                    store_name=elem["store_name"],
                    genre_str=elem["genre"],
                    description=elem["description"],
                    area=elem["area"],
                    rate_str=elem["rate"],
                    coord=elem["coord"],
                    comment_num=elem["comment_num"],
                    save_num_str=elem["save_num"],
                    dinner_budget_str=elem["dinner_budget"],
                    lunch_budget_str=elem["lunch_budget"],
                    url=elem["url"],
                    drink=represent_drink,
                )
            )
        return store_detail_list
