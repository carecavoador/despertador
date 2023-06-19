from dataclasses import dataclass


@dataclass
class Alarme:
    id: int
    description: str
    hour: int
    minutes: int
