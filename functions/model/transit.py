from dataclasses import dataclass, asdict


@dataclass
class Transit:
    org_station_id: str
    dst_station_id: str
    transit_time_sec: int
    station_id_sequence: str

    @staticmethod
    def to_dict(obj):
        return asdict(obj)
