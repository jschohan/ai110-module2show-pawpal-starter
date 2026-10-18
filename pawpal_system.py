from dataclasses import dataclass, field
from datetime import time
from typing import List


@dataclass
class Task:
    name: str
    priority: int
    time: time


@dataclass
class Pet:
    name: str
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)


@dataclass
class Scheduler:
    owner: Owner

    def generate_daily_plan(self) -> List[Task]:
        pass
