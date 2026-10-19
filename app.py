import streamlit as st
from datetime import time
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session "vault": create each object only once per session ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

# --- Owner ---
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# --- Pets ---
st.subheader("Pets")
new_pet_name = st.text_input("Pet name", value="Mochi")
if st.button("Add pet"):
    name = new_pet_name.strip()
    if not name:
        st.error("Pet name can't be empty.")
    elif any(p.name == name for p in owner.pets):
        st.warning(f"{name} is already on your list.")
    else:
        owner.add_pet(Pet(name=name))
        st.success(f"Added {name}!")

if owner.pets:
    st.write("Your pets: " + ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Tasks ---
st.subheader("Tasks")
if not owner.pets:
    st.caption("Add a pet before creating tasks.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pet_choice = st.selectbox("Pet", [p.name for p in owner.pets])
    with col2:
        description = st.text_input("Task", value="Morning walk")
    with col3:
        task_time = st.time_input("Time", value=time(8, 0))
    with col4:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        if not description.strip():
            st.error("Task description can't be empty.")
        else:
            pet = next(p for p in owner.pets if p.name == pet_choice)
            pet.add_task(
                Task(description=description.strip(), time=task_time, frequency=frequency)
            )
            st.success(f"Added '{description.strip()}' for {pet.name}.")

# Task list with filter and completion toggles
all_tasks = scheduler.get_all_tasks()
if all_tasks:
    st.markdown("#### Current tasks")
    filter_choice = st.selectbox(
        "Filter by pet", ["All"] + [p.name for p in owner.pets], key="filter_pet"
    )
    shown = (
        scheduler.sort_by_time()
        if filter_choice == "All"
        else scheduler.sort_by_time(scheduler.filter_by_pet(filter_choice))
    )
    for i, task in enumerate(shown):
        # id() keeps keys unique and stable for each task object
        done = st.checkbox(
            f"{task.time.strftime('%H:%M')} — {task.description} "
            f"({task.pet_name}, {task.frequency})",
            value=task.completed,
            key=f"task_done_{id(task)}",
        )
        if done != task.completed:
            if done:
                if scheduler.mark_task_complete(task):
                    st.rerun()  # show the newly created next occurrence
            else:
                task.mark_incomplete()
else:
    st.info("No tasks yet.")

st.divider()

# --- Schedule ---
st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    plan = scheduler.generate_daily_plan()
    if not plan:
        st.info("Nothing pending. Add tasks or mark some incomplete.")
    else:
        st.table(
            [
                {
                    "Time": t.time.strftime("%H:%M"),
                    "Pet": t.pet_name,
                    "Task": t.description,
                    "Frequency": t.frequency,
                }
                for t in plan
            ]
        )
