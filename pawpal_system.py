from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, date
from typing import List, Optional


def _parse_time(time_str: str) -> datetime:
    """Parse a time string into a datetime object for arithmetic comparisons."""
    for fmt in ("%H:%M", "%I:%M %p", "%I:%M%p"):
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized time format: {time_str!r}")


@dataclass
class Task:
    description: str
    time: str           # Expected format: "HH:MM" e.g. "09:00"
    duration: int       # In minutes
    priority: int       # 1 = highest, 3 = lowest
    category: str
    is_completed: bool = False
    pet_name: str = ""      # Stamped automatically by Pet.add_task()
    frequency: str = "Once" # "Once", "Daily", "Weekly"
    date: str = ""          # "YYYY-MM-DD"; empty means today

    def mark_complete(self, pet: Optional["Pet"] = None) -> None:
        """Mark this task done; if recurring, schedule the next occurrence on the pet."""
        self.is_completed = True
        if self.frequency in ("Daily", "Weekly") and pet is not None:
            base = date.fromisoformat(self.date) if self.date else date.today()
            delta = timedelta(days=1) if self.frequency == "Daily" else timedelta(weeks=1)
            next_task = replace(self, date=(base + delta).isoformat(), is_completed=False)
            pet.add_task(next_task)


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Stamp the task with this pet's name and append it to the task list."""
        task.pet_name = self.name
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's roster."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of every task across all owned pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:

    def generate_daily_plan(self, owner: Owner, include_completed: bool = True) -> List[Task]:
        """Return the owner's tasks sorted; pass include_completed=False for a pending-only view."""
        tasks = owner.get_all_tasks()
        if not include_completed:
            tasks = self.filter_tasks(tasks, show_completed=False)
        return self.sort_tasks_by_priority(tasks)

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort by completed status (pending first), then priority (1 first), then start time."""
        return sorted(tasks, key=lambda t: (t.is_completed, t.priority, _parse_time(t.time)))

    def filter_tasks(self, tasks: List[Task], show_completed: bool = False) -> List[Task]:
        """Return only tasks whose completed status matches show_completed."""
        return [t for t in tasks if t.is_completed == show_completed]

    def detect_conflicts(self, tasks: List[Task]) -> List[tuple]:
        """Return pairs of tasks that overlap in time for the same pet."""
        # Group tasks by pet so we only check overlaps within the same pet's schedule
        pet_tasks: dict = {}
        for task in tasks:
            pet_tasks.setdefault(task.pet_name, []).append(task)

        conflicts: List[tuple] = []
        for pet_task_list in pet_tasks.values():
            sorted_tasks = sorted(pet_task_list, key=lambda t: _parse_time(t.time))
            for i in range(len(sorted_tasks)):
                for j in range(i + 1, len(sorted_tasks)):
                    a = sorted_tasks[i]
                    b = sorted_tasks[j]
                    a_start = _parse_time(a.time)
                    a_end = a_start + timedelta(minutes=a.duration)
                    b_start = _parse_time(b.time)
                    if b_start < a_end:   # b starts before a finishes → overlap
                        conflicts.append((a, b))
        return conflicts
