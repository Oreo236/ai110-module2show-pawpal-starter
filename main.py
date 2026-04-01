from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Alex", daily_available_minutes=120)

    # Create pets
    pet1 = Pet(name="Buddy", species="dog", age=4)
    pet2 = Pet(name="Mittens", species="cat", age=2)

    # Register pets with owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Create tasks
    t1 = Task(name="Morning Walk", duration=30, priority=3, category="walking", preferred_time="morning")
    t2 = Task(name="Feed Breakfast", duration=10, priority=5, category="feeding", must_do=True, preferred_time="morning")
    t3 = Task(name="Medicate", duration=5, priority=10, category="meds", must_do=True)
    t4 = Task(name="Play Session", duration=25, priority=2, category="enrichment", preferred_time="evening")

    # Assign tasks to pets
    pet1.add_task(t1)
    pet1.add_task(t2)
    pet1.add_task(t4)
    pet2.add_task(t3)

    # Run scheduler
    scheduler = Scheduler(owner, [pet1, pet2])
    schedule = scheduler.generate_schedule()

    # Output
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


if __name__ == "__main__":
    main()
