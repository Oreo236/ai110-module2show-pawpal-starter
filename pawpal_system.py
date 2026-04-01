from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union


@dataclass
class Task:
    name: str
    duration: int  # minutes
    priority: int = 1
    category: str = "general"
    completed: bool = False
    must_do: bool = False
    preferred_time: Optional[str] = None  # e.g., "morning", "afternoon"

    def mark_complete(self) -> None:
        """Mark the task complete."""
        ...

    def update_priority(self, new_priority: int) -> None:
        ...

    def update_duration(self, new_duration: int) -> None:
        ...

    def is_mandatory(self) -> bool:
        ...


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        ...

    def remove_task(self, task_name: str) -> None:
        ...

    def get_tasks(self) -> List[Task]:
        ...

    def get_tasks_by_category(self, category: str) -> List[Task]:
        ...


@dataclass
class Owner:
    name: str
    daily_available_minutes: int
    preferences: Dict[str, Union[str, int, bool]] = field(default_factory=dict)

    def update_availability(self, minutes: int) -> None:
        ...

    def add_preference(self, key: str, value) -> None:
        ...

    def get_preferences(self) -> Dict[str, Union[str, int, bool]]:
        ...


@dataclass
class Schedule:
    tasks: List[Task] = field(default_factory=list)
    total_time: int = 0
    remaining_time: int = 0

    def add_task(self, task: Task) -> None:
        ...

    def remove_task(self, task_name: str) -> None:
        ...

    def calculate_total_time(self) -> int:
        ...

    def summarize(self) -> str:
        ...


class Scheduler:
    """Scheduler coordinates owner/pet tasks and produces a daily plan."""

    def __init__(self, owner: Owner, pets: Union[Pet, List[Pet]]):
        self.owner = owner
        self.pets: List[Pet] = pets if isinstance(pets, list) else [pets]
        self.schedule: Optional[Schedule] = None
        self._unscheduled: List[Task] = []

    def generate_schedule(self) -> Schedule:
        raise NotImplementedError

    def clear_schedule(self) -> None:
        self.schedule = None
        self._unscheduled = []

    def get_schedule(self) -> Optional[Schedule]:
        return self.schedule

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        raise NotImplementedError

    def filter_feasible_tasks(self, tasks: List[Task], available_minutes: int) -> List[Task]:
        raise NotImplementedError

    def apply_preferences(self, tasks: List[Task]) -> List[Task]:
        raise NotImplementedError

    def enforce_mandatory_tasks(self, tasks: List[Task]) -> List[Task]:
        raise NotImplementedError

    def explain_schedule(self) -> Dict[str, str]:
        raise NotImplementedError

    def get_unscheduled_tasks(self) -> List[Task]:
        return list(self._unscheduled)

    def get_total_time_used(self) -> int:
        if self.schedule is None:
            return 0
        return self.schedule.total_time
