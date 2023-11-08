import sqlite3
import sys
from model.transit import Transit

DB_PATH = "./static/transit.db"


class DBAccessor:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
        self.transit_table_name = "transit"

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

    def select_transit_record_by_o(self, org_station_id):
        self.execute_query(
            f"""SELECT * FROM {self.transit_table_name} 
            WHERE org_station_id=\"{org_station_id}\""""
        )
        raw_result_list = self.cur.fetchall()
        return [
            Transit(
                org_station_id=elem[0],
                dst_station_id=elem[1],
                # TODO: DBに入っている値を分単位にする
                transit_time_min=(elem[2] / 60),
                station_id_sequence=elem[3],
            )
            for elem in raw_result_list
        ]
