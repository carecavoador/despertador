from dataclasses import dataclass
from datetime import datetime


@dataclass
class Alarm:
    id: int
    description: str
    next_alarm: datetime
