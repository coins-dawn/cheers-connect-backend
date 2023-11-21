import sqlite3
import sys
from model.store_detail import StoreDetail

DB_PATH = "./static/store.db"


class StoreDetailDBAccessor:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
        self.table_name = "store"

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def execute_query(self, query_str):
        try:
            self.cur.execute(query_str)
        except Exception as e:
            print(query_str)
            print(e)
            sys.exit()

    def filter_by_store_attributes(
        self, budget: int, min_comment_num: int, min_save_num: int, min_rate: float
    ) -> list[StoreDetail]:
        self.execute_query(
            f"""
            SELECT * FROM {self.table_name}
            WHERE
            dinner_budget_lower_limit <= {budget} AND
            comment_num >= {min_comment_num} AND
            save_num >= {min_save_num} AND
            rate >= {min_rate}
            """
        )
        raw_result_list = self.cur.fetchall()
        return [
            StoreDetail(
                id=elem[0],
                store_name=elem[1],
                genre_str=elem[2],
                description=elem[3],
                area=elem[4],
                rate=elem[5],
                coord=elem[6],
                comment_num=elem[7],
                save_num=elem[8],
                dinner_budget_upper_limit=elem[9],
                dinner_budget_lower_limit=elem[10],
                url=elem[11],
            )
            for elem in raw_result_list
        ]
