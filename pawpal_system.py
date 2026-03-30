from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str
    duration: int
    priority: int
    category: str
    is_completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:

    def generate_daily_plan(self, owner: Owner) -> List[Task]:
        pass

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[tuple]:
        pass
