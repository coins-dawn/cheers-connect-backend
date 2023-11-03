from dataclasses import dataclass


@dataclass
class Transit:
    org_station_id: str
    dst_station_id: str
    transit_time_sec: int
    station_id_sequence: str
