from dataclasses import dataclass


@dataclass
class Alarm:
    id: int
    description: str
    hour: int
    minutes: int
