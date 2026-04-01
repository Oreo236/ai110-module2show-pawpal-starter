import streamlit as st
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
        st.experimental_rerun()
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
            st.experimental_rerun()

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

if st.button("Add task"):
    if not st.session_state.get("owner"):
        st.warning("Save an owner to session first.")
    elif not assign_to:
        st.warning("Add a pet first or select an existing pet to assign the task.")
    else:
        # map priority label to numeric
        pmap = {"low": 1, "medium": 2, "high": 3}
        t = Task(name=task_title, duration=int(duration), priority=pmap.get(priority, 2))
        # find pet and add task
        pet_obj = next((p for p in pets if p.name == assign_to), None)
        if pet_obj is None:
            st.error("Selected pet not found.")
        else:
            pet_obj.add_task(t)
            st.success(f"Added task '{t.name}' to {pet_obj.name}")
            st.experimental_rerun()

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
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
