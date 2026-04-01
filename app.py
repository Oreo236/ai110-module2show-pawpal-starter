import streamlit as st
import time
from typing import Any
from pawpal_system import Owner, Pet, Task, Scheduler, Schedule


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()


def _safe_rerun() -> None:
    """Attempt to rerun the Streamlit script.

    Some Streamlit versions expose `st.experimental_rerun()`. If it's not
    available in the user's environment, we fall back to toggling a query
    parameter which triggers a rerun.
    """
    try:
        # Preferred API when available
        st.experimental_rerun()
    except Exception:
        # Fallback: change query params to force a rerun
        try:
            params = st.experimental_get_query_params() or {}
            params["_rerun"] = int(time.time() * 1000)
            st.experimental_set_query_params(**params)
        except Exception:
            # As a last resort, do nothing; user can refresh manually
            return

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Session-managed owner: check and create
if "owner" not in st.session_state:
    st.session_state.owner = None

daily_minutes = st.number_input("Owner: daily available minutes", min_value=0, value=120)

if st.button("Save owner to session"):
    st.session_state.owner = Owner(name=owner_name, daily_available_minutes=int(daily_minutes))

if st.session_state.owner:
    owner = st.session_state.owner
    st.success(f"Owner in session: {owner.name} — {owner.daily_available_minutes} minutes/day")
    if st.button("Clear owner from session"):
        del st.session_state["owner"]
        _safe_rerun()
else:
    st.info("No Owner stored in session. Use 'Save owner to session' to create one.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Show pets from owner in session
pets = []
if st.session_state.get("owner"):
    pets = st.session_state.owner.get_pets()

col_pet_left, col_pet_right = st.columns(2)
with col_pet_left:
    # Add pet UI: uses Owner.add_pet
    if st.button("Add pet"):
        if not st.session_state.get("owner"):
            st.warning("Save an owner to session first.")
        else:
            new_pet = Pet(name=pet_name, species=species, age=1)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added pet {new_pet.name}")
            _safe_rerun()

with col_pet_right:
    # Select which pet to assign tasks to
    pet_names = [p.name for p in pets]
    if pet_names:
        assign_to = st.selectbox("Assign task to pet", pet_names)
    else:
        assign_to = None

# Task inputs
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        
col_time = st.text_input("Start time (HH:MM, optional)", value="", max_chars=5)

if st.button("Add task"):
    if not st.session_state.get("owner"):
        st.warning("Save an owner to session first.")
    elif not assign_to:
        st.warning("Add a pet first or select an existing pet to assign the task.")
    else:
        # map priority label to numeric
        pmap = {"low": 1, "medium": 2, "high": 3}
        t = Task(name=task_title, duration=int(duration), priority=pmap.get(priority, 2))
        # set optional time if provided (validate HH:MM)
        if col_time:
            try:
                h, m = col_time.split(":")
                hh = int(h)
                mm = int(m)
                if 0 <= hh <= 23 and 0 <= mm <= 59:
                    # normalize to zero-padded format
                    t.time = f"{hh:02d}:{mm:02d}"
                else:
                    st.warning("Time must be in HH:MM (00:00–23:59) format. Ignoring time input.")
            except Exception:
                st.warning("Time must be in HH:MM format. Ignoring time input.")
        # find pet and add task
        pet_obj = next((p for p in pets if p.name == assign_to), None)
        if pet_obj is None:
            st.error("Selected pet not found.")
        else:
            pet_obj.add_task(t)
            st.success(f"Added task '{t.name}' to {pet_obj.name}")
            _safe_rerun()

# Display current pets and their tasks
if pets:
    st.write("Current pets and tasks:")
    for p in pets:
        st.markdown(f"**{p.name}** ({p.species}) — {len(p.tasks)} tasks")
        if p.tasks:
            for tt in p.tasks:
                st.write(f"- {tt.name} — {tt.duration}m — priority {tt.priority}")
        else:
            st.info("No tasks for this pet yet.")
else:
    st.info("No pets yet. Add one using the 'Add pet' button.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan and view conflicts or explanations.")

# Filters for the displayed tasks — placed outside the Generate button so
# adjusting filters won't force the user to regenerate the schedule.
pet_names_all = []
if st.session_state.get("owner"):
    pet_names_all = [p.name for p in st.session_state.owner.get_pets()]
col_f1, col_f2, col_f3 = st.columns([2, 2, 2])
with col_f1:
    pet_filter = st.selectbox("Filter by pet", ["All"] + pet_names_all)
with col_f2:
    completion_filter = st.selectbox("Completion", ["All", "Pending", "Completed"], index=1)
with col_f3:
    # use a slider-like selector with numeric values so comparison is straightforward
    min_priority = st.selectbox("Min priority", ["All", 1, 2, 3], index=0)

# Sorting option
sort_by_time = st.checkbox("Sort schedule by start time", value=True)

if st.button("Generate schedule"):
    if not st.session_state.get("owner"):
        st.warning("Save an owner to session first.")
    else:
        owner = st.session_state.owner
        pets = owner.get_pets()
        if not pets:
            st.info("No pets available to schedule. Add a pet first.")
        else:
            sched = Scheduler(owner, pets)
            schedule = sched.generate_schedule()
            st.session_state["scheduler"] = sched
            st.session_state["schedule"] = schedule

# If a schedule exists in session state, display it and conflicts according
# to the current filters (filtering won't delete the stored schedule).
if st.session_state.get("schedule") and st.session_state.get("scheduler"):
    sched = st.session_state.get("scheduler")
    schedule = st.session_state.get("schedule")
    owner = st.session_state.owner
    pets = owner.get_pets()

    # Build the base task list (all owner's tasks), and then apply filters
    base_tasks = owner.get_all_tasks()
    def task_matches_filters(t):
        if pet_filter != "All":
            # only include tasks belonging to selected pet (by identity)
            owner_pet = next((p for p in owner.get_pets() if p.name == pet_filter), None)
            if owner_pet is None or not any(t is tt for tt in owner_pet.get_tasks()):
                return False
        if completion_filter == "Pending" and t.completed:
            return False
        if completion_filter == "Completed" and not t.completed:
            return False
        if min_priority != "All" and t.priority < int(min_priority):
            return False
        return True

    filtered_tasks_for_checks = [t for t in base_tasks if task_matches_filters(t)]

    # Show conflict warnings prominently so owners can resolve overlaps
    conflicts = sched.detect_time_conflicts(filtered_tasks_for_checks)
    if conflicts:
        st.warning("Some tasks share the same start time. Review conflicts below and adjust times or priorities.")
        with st.expander("View task conflicts", expanded=False):
            for time_str, lst in conflicts.items():
                def owner_name_for(task):
                    for p in pets:
                        if any(task is tt for tt in p.get_tasks()):
                            return p.name
                    return "unknown"

                names = ", ".join(f"{t.name} (pet: {owner_name_for(t)})" for t in lst)
                st.write(f"**{time_str}** — {names}")
            st.markdown("**Suggested actions:** \n- Reschedule one of the conflicting tasks to a different time.\n- Reduce duration or split a task.\n- Mark a task completed if it's already done.")

    # Present schedule (sorted if requested) and apply filters to displayed rows
    if not schedule.tasks:
        st.info("No tasks scheduled for today.")
    else:
        if sort_by_time:
            def sort_key(t):
                tm = getattr(t, "time", "") or "zzzz"
                return (tm, -t.priority, t.duration)
            display_tasks = sorted(schedule.tasks, key=sort_key)
        else:
            display_tasks = list(schedule.tasks)

        display_tasks = [t for t in display_tasks if task_matches_filters(t)]

        hcols = st.columns([1, 2, 3, 2, 2, 2])
        for col, label in zip(hcols, ["Done", "Pet", "Task", "Duration (m)", "Priority", "Time"]):
            col.markdown(f"**{label}**")

        for t in display_tasks:
            pet_label = next((p.name for p in pets if any(t is tt for tt in p.get_tasks())), "(unknown)")
            rcols = st.columns([1, 2, 3, 2, 2, 2])
            checked = rcols[0].checkbox("", value=t.completed, key=f"complete_{id(t)}", label_visibility="collapsed")
            if checked != t.completed:
                t.completed = checked
            task_label = f"~~{t.name}~~" if t.completed else t.name
            rcols[1].write(pet_label)
            rcols[2].write(task_label)
            rcols[3].write(t.duration)
            rcols[4].write(t.priority)
            rcols[5].write(getattr(t, "time", "") or "—")

        # Explanations for why tasks were chosen or skipped (per-pet)
        st.markdown("**Explanation**")
        expl_rows = []
        for t in schedule.tasks:
            pet_name = next((p.name for p in pets if any(t is tt for tt in p.get_tasks())), "(unknown)")
            expl_rows.append({"Pet": pet_name, "Task": t.name, "Reason": f"Selected (priority {t.priority}, {t.duration}m)"})
        for t in sched.get_unscheduled_tasks():
            pet_name = next((p.name for p in pets if any(t is tt for tt in p.get_tasks())), "(unknown)")
            expl_rows.append({"Pet": pet_name, "Task": t.name, "Reason": f"Not selected (priority {t.priority}, {t.duration}m)"})

        if expl_rows:
            st.table(expl_rows)
        else:
            st.write("No explanation available.")
