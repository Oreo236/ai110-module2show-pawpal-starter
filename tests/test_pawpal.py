import pytest
import sys
import os
from datetime import date, timedelta

# Ensure project root is on sys.path so tests can import modules in repository
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    t = Task(name="Feed", duration=10)
    assert t.completed is False
    t.mark_complete()
    assert t.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog", age=4)
    before = len(pet.get_tasks())
    pet.add_task(Task(name="Walk", duration=20))
    after = len(pet.get_tasks())
    assert after == before + 1


def test_sorting_correctness():
    owner = Owner(name="Alice", daily_available_minutes=60)
    pet = Pet(name="Buddy", species="dog", age=4)

    t1 = Task(name="A", duration=10)
    t1.time = "09:00"
    t2 = Task(name="B", duration=5)
    t2.time = "08:30"
    t3 = Task(name="C", duration=5)  # no time -> should sort last

    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)
    owner.add_pet(pet)

    sched = Scheduler(owner, [pet])
    sorted_tasks = sched.sort_by_time(pet.get_tasks())

    times = [getattr(t, "time", None) for t in sorted_tasks]
    assert times[0] == "08:30"
    assert times[1] == "09:00"
    assert sorted_tasks[-1].name == "C"


def test_recurrence_logic_creates_next_day():
    owner = Owner(name="Alice", daily_available_minutes=60)
    pet = Pet(name="Buddy", species="dog", age=4)

    orig_due = date.today()
    t = Task(name="Med", duration=5, frequency="daily", due_date=orig_due)
    pet.add_task(t)
    owner.add_pet(pet)

    sched = Scheduler(owner, [pet])
    new_task = sched.mark_task_complete(t, pet_name=pet.name)

    assert t.completed is True
    assert new_task is not None
    assert new_task.due_date == orig_due + timedelta(days=1)
    assert new_task.completed is False


def test_conflict_detection_flags_duplicate_times():
    owner = Owner(name="Alice", daily_available_minutes=120)
    pet = Pet(name="Buddy", species="dog", age=4)

    t1 = Task(name="Morning Walk", duration=20)
    t1.time = "07:00"
    t2 = Task(name="Breakfast", duration=10)
    t2.time = "07:00"

    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)

    sched = Scheduler(owner, [pet])
    conflicts = sched.detect_time_conflicts()

    assert "07:00" in conflicts
    assert len(conflicts["07:00"]) == 2
    warnings = sched.conflict_warnings()
    assert any("07:00" in w for w in warnings)


def test_generate_schedule_happy_path():
    owner = Owner(name="Sam", daily_available_minutes=60)
    pet = Pet(name="Milo", species="cat", age=3)

    t_mand = Task(name="Feed", duration=15)
    t_mand.must_do = True
    t_high = Task(name="Play", duration=20, priority=3)
    t_low = Task(name="Groom", duration=30, priority=1)

    pet.add_task(t_mand)
    pet.add_task(t_high)
    pet.add_task(t_low)
    owner.add_pet(pet)

    sched = Scheduler(owner, [pet])
    schedule = sched.generate_schedule()

    # mandatory should be included, then highest-priority fits next
    names = [t.name for t in schedule.tasks]
    assert "Feed" in names
    assert "Play" in names
    # Groom may or may not fit (15+20=35 -> remaining 25, so Groom won't fit)
    assert schedule.remaining_time == 60 - sum(t.duration for t in schedule.tasks)


def test_pet_with_no_tasks_generates_empty_schedule():
    owner = Owner(name="Zoe", daily_available_minutes=45)
    pet = Pet(name="Empty", species="fish", age=1)
    owner.add_pet(pet)

    sched = Scheduler(owner, [pet])
    schedule = sched.generate_schedule()

    assert schedule.tasks == []
    assert schedule.remaining_time == 45


def test_mark_nonrecurring_returns_none_and_marks_complete():
    owner = Owner(name="A", daily_available_minutes=30)
    pet = Pet(name="Solo", species="bird", age=2)
    t = Task(name="OneOff", duration=5)
    pet.add_task(t)
    owner.add_pet(pet)

    sched = Scheduler(owner, [pet])
    res = sched.mark_task_complete(t, pet_name=pet.name)

    assert t.completed is True
    assert res is None


def test_conflicts_ignore_completed_tasks():
    owner = Owner(name="Lila", daily_available_minutes=90)
    pet = Pet(name="Buddy", species="dog", age=5)

    t1 = Task(name="Walk", duration=20)
    t1.time = "10:00"
    t2 = Task(name="Vet", duration=30)
    t2.time = "10:00"

    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)

    sched = Scheduler(owner, [pet])
    # mark one completed; detection should ignore it
    sched.mark_task_complete(t1, pet_name=pet.name)
    conflicts = sched.detect_time_conflicts()
    assert "10:00" not in conflicts
