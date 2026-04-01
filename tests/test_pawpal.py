import pytest

from pawpal_system import Task, Pet


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
