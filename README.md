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

## Features

### Schedule Generation
- **Priority-first scheduling** — Mandatory tasks (`must_do=True`) are always placed first; remaining tasks are sorted by priority (high → low) then by shorter duration to maximize tasks that fit within the owner's daily available minutes.
- **Time budget enforcement** — Tasks that exceed the remaining available minutes are moved to an "unscheduled" list and surfaced in the UI explanation.

### Sorting & Filtering
- **Sort by start time** — Tasks can be ordered chronologically using an `HH:MM` time attribute; tasks without a time are pushed to the end.
- **Sort by priority** — Tasks can be reordered by priority (descending) with duration as a tiebreaker.
- **Filter by pet** — View only tasks belonging to a specific pet.
- **Filter by completion** — Toggle between pending, completed, or all tasks.
- **Filter by minimum priority** — Hide tasks below a chosen priority threshold.
- **Feasibility filter** — Greedily selects the subset of tasks that fits within a given time budget.

### Conflict Detection
- **Time conflict detection** — Identifies tasks that share the same `HH:MM` start time across all pets; completed tasks are excluded from conflict checks.
- **Human-readable conflict warnings** — Generates plain-English warning strings (e.g., "Conflict at 08:00: Morning walk, Feeding") for display in the UI.

### Recurring Tasks
- **Daily & weekly recurrence** — When `Scheduler.mark_task_complete()` is called on a task with `frequency="daily"` or `frequency="weekly"`, it automatically creates the next occurrence with an updated `due_date` and adds it to the pet.

### Owner Preferences
- **Preferred time-of-day ordering** — If an owner sets a `preferred_time` preference (e.g., `"morning"`), tasks matching that preference are surfaced first during schedule generation.

### Task Completion
- **Mark tasks complete** — Each scheduled task has an inline checkbox in the UI; checking it calls `task.completed = True`, which immediately removes it from conflict checks and pending filters.

### Plan Explanation
- **Schedule explanation** — Every task in the generated plan includes a reason (priority level and duration); unscheduled tasks show why they were skipped.

## Demo

<a href="/course_images/ai110/paw-starter.png" target="_blank"><img src='/course_images/ai110/paw-starter.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.