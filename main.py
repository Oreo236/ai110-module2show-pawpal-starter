from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date


def main() -> None:
    owner = Owner(name="Alex", daily_available_minutes=120)

    pet1 = Pet(name="Buddy", species="dog", age=4)
    pet2 = Pet(name="Mittens", species="cat", age=2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    t1 = Task(name="Morning Walk", duration=30, priority=3, category="walking", preferred_time="morning")
    t1.time = "07:30"

    t2 = Task(name="Feed Breakfast", duration=10, priority=5, category="feeding", must_do=True, preferred_time="morning")
    t2.time = "08:00"
    t2.frequency = "daily"
    t2.due_date = date.today()

    t3 = Task(name="Medicate", duration=5, priority=10, category="meds", must_do=True)
    t3.time = "12:15"

    t4 = Task(name="Play Session", duration=25, priority=2, category="enrichment", preferred_time="evening")
    t4.time = "07:30"

    pet1.add_task(t4)
    pet1.add_task(t1)
    pet2.add_task(t3)
    pet1.add_task(t2)

    scheduler = Scheduler(owner, [pet1, pet2])
    schedule = scheduler.generate_schedule()

    print("Today's Schedule:\n")
    print(schedule.summarize())
    print(f"\nTotal time used: {schedule.total_time} minutes")
    print(f"Remaining time: {schedule.remaining_time} minutes\n")

    print("Explanation:")
    for name, reason in scheduler.explain_schedule().items():
        print(f"- {name}: {reason}")

    uns = scheduler.get_unscheduled_tasks()
    if uns:
        print("\nUnscheduled tasks:")
        for t in uns:
            print(f"- {t.name} ({t.duration}m) priority {t.priority}")

    print("\nAll tasks (original order):")
    for t in owner.get_all_tasks():
        print(f"- {t.name} @ {getattr(t, 'time', None)} completed={t.completed}")

    print("\nAll tasks (sorted by time):")
    for t in scheduler.sort_by_time(owner.get_all_tasks()):
        print(f"- {t.name} @ {getattr(t, 'time', None)} completed={t.completed}")

    print("\nIncomplete tasks:")
    for t in scheduler.filter_tasks(completed=False):
        print(f"- {t.name} @ {getattr(t, 'time', None)} completed={t.completed}")

    print("\nTasks for Buddy:")
    for t in scheduler.filter_tasks(pet_name="Buddy"):
        print(f"- {t.name} @ {getattr(t, 'time', None)} completed={t.completed}")

    # Now mark Feed Breakfast complete via Scheduler to trigger recurrence
    new_occurrence = scheduler.mark_task_complete(t2, pet_name="Buddy")
    if new_occurrence:
        print(f"\nCreated recurring task: {new_occurrence.name} due {new_occurrence.due_date}")
    else:
        print("\nNo recurring task created.")

    warnings = scheduler.conflict_warnings()
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"- {w}")
    else:
        print("\nNo time conflicts detected.")


if __name__ == "__main__":
    main()
