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
        self.completed = True

    def update_priority(self, new_priority: int) -> None:
        """Update the task's priority level."""
        self.priority = int(new_priority)

    def update_duration(self, new_duration: int) -> None:
        """Update the task's duration in minutes."""
        self.duration = int(new_duration)

    def is_mandatory(self) -> bool:
        """Return True if the task is marked mandatory."""
        return bool(self.must_do)


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove tasks with the given name from this pet."""
        self.tasks = [t for t in self.tasks if t.name != task_name]

    def get_tasks(self) -> List[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Return tasks filtered by the given category."""
        return [t for t in self.tasks if t.category == category]


@dataclass
class Owner:
    name: str
    daily_available_minutes: int
    preferences: Dict[str, Union[str, int, bool]] = field(default_factory=dict)

    def update_availability(self, minutes: int) -> None:
        """Set the owner's daily available minutes for pet care."""
        self.daily_available_minutes = int(minutes)

    def add_preference(self, key: str, value) -> None:
        """Add or update an owner preference key/value."""
        self.preferences[key] = value

    def get_preferences(self) -> Dict[str, Union[str, int, bool]]:
        """Return a copy of the owner's preferences."""
        return dict(self.preferences)

    # Pet management helpers
    def add_pet(self, pet: 'Pet') -> None:
        """Register a pet under this owner."""
        if not hasattr(self, '_pets'):
            self._pets: List[Pet] = []
        self._pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name from this owner."""
        if not hasattr(self, '_pets'):
            return
        self._pets = [p for p in self._pets if p.name != pet_name]

    def get_pets(self) -> List['Pet']:
        """Return the list of pets registered to this owner."""
        return list(getattr(self, '_pets', []))

    def get_all_tasks(self) -> List[Task]:
        """Collect and return all tasks from every pet of this owner."""
        tasks: List[Task] = []
        for p in self.get_pets():
            tasks.extend(p.get_tasks())
        return tasks


@dataclass
class Schedule:
    tasks: List[Task] = field(default_factory=list)
    total_time: int = 0
    remaining_time: int = 0

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove a task from the schedule by name."""
        self.tasks = [t for t in self.tasks if t.name != task_name]

    def calculate_total_time(self) -> int:
        """Recalculate and return the schedule's total time."""
        self.total_time = sum(t.duration for t in self.tasks)
        return self.total_time

    def summarize(self) -> str:
        """Return a human-readable summary of scheduled tasks."""
        if not self.tasks:
            return "(no tasks scheduled)"
        lines = [f"{t.name} — {t.duration}m — priority {t.priority}" for t in self.tasks]
        return "\n".join(lines)


class Scheduler:
    """Scheduler coordinates owner/pet tasks and produces a daily plan."""

    def __init__(self, owner: Owner, pets: Union[Pet, List[Pet]]):
        self.owner = owner
        self.pets: List[Pet] = pets if isinstance(pets, list) else [pets]
        self.schedule: Optional[Schedule] = None
        self._unscheduled: List[Task] = []

    def generate_schedule(self) -> Schedule:
        """Generate a daily schedule based on owner constraints and priorities."""
        # Gather all tasks from the owner
        all_tasks: List[Task] = self.owner.get_all_tasks()

        # Ensure mandatory tasks are included first
        mandatory = [t for t in all_tasks if t.is_mandatory()]
        remaining = [t for t in all_tasks if not t.is_mandatory()]

        # Sort remaining tasks by priority (high -> low), then shorter duration
        remaining_sorted = sorted(remaining, key=lambda t: (-t.priority, t.duration))

        available = int(self.owner.daily_available_minutes)

        schedule = Schedule()

        # Add mandatory tasks first (if they fit)
        for t in mandatory:
            if t.duration <= available:
                schedule.add_task(t)
                available -= t.duration
            else:
                # can't fit mandatory task; still mark as unscheduled
                self._unscheduled.append(t)

        # Add as many high-priority tasks as fit
        for t in remaining_sorted:
            if t.duration <= available:
                schedule.add_task(t)
                available -= t.duration
            else:
                self._unscheduled.append(t)

        schedule.remaining_time = available
        self.schedule = schedule
        return schedule

    def clear_schedule(self) -> None:
        """Clear the current schedule and any unscheduled task list."""
        self.schedule = None
        self._unscheduled = []

    def get_schedule(self) -> Optional[Schedule]:
        """Return the last generated schedule, or None if none exists."""
        return self.schedule

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by priority (high->low) then by shorter duration."""
        return sorted(tasks, key=lambda t: (-t.priority, t.duration))

    def filter_feasible_tasks(self, tasks: List[Task], available_minutes: int) -> List[Task]:
        """Greedily select tasks that fit within available minutes."""
        feasible: List[Task] = []
        remaining = available_minutes
        for t in sorted(tasks, key=lambda x: (x.duration, -x.priority)):
            if t.duration <= remaining:
                feasible.append(t)
                remaining -= t.duration
        return feasible

    def apply_preferences(self, tasks: List[Task]) -> List[Task]:
        """Reorder tasks to respect simple owner time-of-day preferences."""
        # Simple preference handling: if owner prefers morning tasks, keep tasks
        # that match preferred_time first. Preferences can be extended later.
        pref_time = self.owner.preferences.get("preferred_time")
        if not pref_time:
            return tasks
        preferred = [t for t in tasks if t.preferred_time == pref_time]
        others = [t for t in tasks if t.preferred_time != pref_time]
        return preferred + others

    def enforce_mandatory_tasks(self, tasks: List[Task]) -> List[Task]:
        """Move mandatory tasks to the front of the task list."""
        mandatory = [t for t in tasks if t.is_mandatory()]
        optional = [t for t in tasks if not t.is_mandatory()]
        return mandatory + optional

    def explain_schedule(self) -> Dict[str, str]:
        """Return brief explanations for why tasks were selected or skipped."""
        if self.schedule is None:
            return {"error": "No schedule generated"}
        explanation: Dict[str, str] = {}
        for t in self.schedule.tasks:
            explanation[t.name] = f"Selected (priority {t.priority}, {t.duration}m)"
        for t in self._unscheduled:
            explanation[t.name] = f"Not selected (priority {t.priority}, {t.duration}m)"
        return explanation

    def get_unscheduled_tasks(self) -> List[Task]:
        """Return tasks that were considered but not scheduled."""
        return list(self._unscheduled)

    def get_total_time_used(self) -> int:
        """Return the total scheduled time in minutes (0 if none)."""
        if self.schedule is None:
            return 0
        return self.schedule.total_time
