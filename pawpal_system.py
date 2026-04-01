from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from datetime import date, timedelta


@dataclass
class Task:
    name: str
    duration: int  # minutes
    priority: int = 1
    category: str = "general"
    completed: bool = False
    must_do: bool = False
    preferred_time: Optional[str] = None  # e.g., "morning", "afternoon"
    frequency: Optional[str] = None  # e.g., "daily", "weekly"
    due_date: Optional[date] = None

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
        # calculate and store total scheduled time
        schedule.calculate_total_time()

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

    def sort_by_time(self, tasks: List[Task], reverse: bool = False) -> List[Task]:
        """Sort Task objects by their `time` attribute formatted as "HH:MM".

        Tasks without a `time` attribute or with None/invalid format are pushed to the end.
        """
        keyed = []
        for t in tasks:
            tm = getattr(t, "time", None)
            if not tm:
                score = float("inf")
            else:
                try:
                    h, m = tm.split(":")
                    score = int(h) * 60 + int(m)
                except Exception:
                    score = float("inf")
            keyed.append((score, t))
        keyed.sort(key=lambda x: x[0], reverse=reverse)
        return [t for _, t in keyed]

    def filter_feasible_tasks(self, tasks: List[Task], available_minutes: int) -> List[Task]:
        """Greedily select tasks that fit within available minutes."""
        feasible: List[Task] = []
        remaining = available_minutes
        for t in sorted(tasks, key=lambda x: (x.duration, -x.priority)):
            if t.duration <= remaining:
                feasible.append(t)
                remaining -= t.duration
        return feasible

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name.

        - If `completed` is not None, only tasks with `task.completed == completed` are returned.
        - If `pet_name` is provided, only tasks belonging to that pet are considered.
        - If both filters are None, all tasks for the owner are returned.
        """
        results: List[Task] = []
        for pet in self.owner.get_pets():
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def mark_task_complete(self, task: Task, pet_name: Optional[str] = None) -> Optional[Task]:
        """Mark a task complete; if it is recurring ('daily' or 'weekly'), create the next occurrence.

        Returns the newly created Task for the next occurrence, or None if no recurrence.
        If `pet_name` is provided, the task will be searched for among that pet's tasks;
        otherwise we search all pets and stop at the first match.
        """
        target_pet = None
        for pet in self.owner.get_pets():
            if pet_name is not None and pet.name != pet_name:
                continue
            # match by identity or by name
            for t in pet.get_tasks():
                if t is task or (t.name == task.name and t.duration == task.duration and t.priority == task.priority):
                    target_pet = pet
                    matched_task = t
                    break
            if target_pet:
                break

        if not target_pet:
            return None

        # mark completed
        matched_task.mark_complete()

        freq = (matched_task.frequency or "").lower()
        if freq not in ("daily", "weekly"):
            return None

        # compute next due date (use today if no due_date set)
        base = matched_task.due_date or date.today()
        delta_days = 1 if freq == "daily" else 7
        next_due = base + timedelta(days=delta_days)

        # create a new Task instance for the next occurrence
        new_task = Task(
            name=matched_task.name,
            duration=matched_task.duration,
            priority=matched_task.priority,
            category=matched_task.category,
            completed=False,
            must_do=matched_task.must_do,
            preferred_time=matched_task.preferred_time,
            frequency=matched_task.frequency,
            due_date=next_due,
        )

        target_pet.add_task(new_task)
        return new_task

    def detect_time_conflicts(self, tasks: Optional[List[Task]] = None) -> Dict[str, List[Task]]:
        """Detect tasks that share the same start time ("HH:MM").

        Returns a dict mapping time string -> list of conflicting Task objects (length > 1).
        If `tasks` is None, considers all owner's tasks.
        Completed tasks are ignored.
        """
        tasks_to_check = tasks if tasks is not None else self.owner.get_all_tasks()
        buckets: Dict[str, List[Task]] = {}
        for t in tasks_to_check:
            tm = getattr(t, "time", None)
            if not tm:
                continue
            if t.completed:
                continue
            buckets.setdefault(tm, []).append(t)

        # filter only times with more than one task
        conflicts = {time: lst for time, lst in buckets.items() if len(lst) > 1}
        return conflicts

    def conflict_warnings(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Return human-readable warning strings for detected time conflicts."""
        conflicts = self.detect_time_conflicts(tasks)
        warnings: List[str] = []
        for time_str, lst in conflicts.items():
            names = ", ".join(f"{t.name}" for t in lst)
            warnings.append(f"Conflict at {time_str}: {names}")
        return warnings

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
    

