# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling
1. Time-based sorting: Orders tasks by an "HH:MM" time attribute so plans can be presented chronologically.
2. Filtering helpers: Filters tasks by completion status or pet name for quick views and UI controls.
3. Recurring tasks: Tasks can have a frequency(daily/weekly) and due_date; calling Scheduler.mark_task_complete will automatically create the next occurrence.
4. Conflict detection: Report tasks that share the same start time to help the owner resolve overlaps.

## Testing PawPal+

- **Run tests:** run: python -m pytest

- **What the tests cover:** Sorting (chronological ordering and handling tasks without times), recurrence logic (marking a daily task complete creates the next occurrence), conflict detection (duplicate start times and warnings), schedule generation (mandatory vs prioritized tasks), and edge cases (pets with no tasks, completed tasks ignored when detecting conflicts).

- **Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — Tests cover core scheduling behaviors and important edge cases