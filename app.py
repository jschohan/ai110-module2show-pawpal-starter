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

# --- Conflict warnings (Scheduler.detect_conflicts) ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.markdown("#### Scheduling conflicts")
    for msg in conflicts:
        st.warning(
            msg.removeprefix("Warning: ")
            + "  \nConsider moving one of these to a different time.",
            icon="⚠️",
        )
elif scheduler.get_pending_tasks():
    st.success("No scheduling conflicts. Your pending tasks don't overlap.")

# --- Task list: filter (Scheduler.filter_tasks) + sort (Scheduler.sort_by_time) ---
if scheduler.get_all_tasks():
    st.markdown("#### Current tasks")
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        filter_pet = st.selectbox(
            "Filter by pet", ["All"] + [p.name for p in owner.pets], key="filter_pet"
        )
    with fcol2:
        filter_status = st.selectbox(
            "Filter by status", ["All", "Pending", "Completed"], key="filter_status"
        )

    shown = scheduler.sort_by_time(
        scheduler.filter_tasks(
            completed={"All": None, "Pending": False, "Completed": True}[filter_status],
            pet_name=None if filter_pet == "All" else filter_pet,
        )
    )

    pending_n = len(scheduler.get_pending_tasks())
    total_n = len(scheduler.get_all_tasks())
    m1, m2, m3 = st.columns(3)
    m1.metric("Total tasks", total_n)
    m2.metric("Pending", pending_n)
    m3.metric("Completed", total_n - pending_n)

    if not shown:
        st.info("No tasks match these filters.")
    else:
        st.caption(f"Showing {len(shown)} task(s), sorted by time.")
        st.table(
            [
                {
                    "Time": t.time.strftime("%H:%M"),
                    "Date": t.due_date.isoformat(),
                    "Pet": t.pet_name,
                    "Task": t.description,
                    "Frequency": t.frequency,
                    "Status": "✅ Done" if t.completed else "⏳ Pending",
                }
                for t in shown
            ]
        )

        with st.expander("Mark tasks complete / incomplete"):
            for task in shown:
                # id() keeps keys unique and stable for each task object
                done = st.checkbox(
                    f"{task.time.strftime('%H:%M')} — {task.description} "
                    f"({task.pet_name}, {task.frequency})",
                    value=task.completed,
                    key=f"task_done_{id(task)}",
                )
                if done != task.completed:
                    if done:
                        nxt = scheduler.mark_task_complete(task)
                        st.session_state["flash"] = (
                            f"Completed '{task.description}'."
                            + (
                                f" Next {nxt.frequency} occurrence scheduled for {nxt.due_date}."
                                if nxt
                                else ""
                            )
                        )
                    else:
                        task.mark_incomplete()
                    st.rerun()  # refresh table, metrics and conflicts

    if "flash" in st.session_state:
        st.success(st.session_state.pop("flash"))
else:
    st.info("No tasks yet.")

st.divider()

# --- Schedule (Scheduler.generate_daily_plan) ---
st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    plan = scheduler.generate_daily_plan()
    if not plan:
        st.info("Nothing pending. Add tasks or mark some incomplete.")
    else:
        st.success(f"{len(plan)} task(s) planned for today, in time order.")
        if conflicts:
            st.warning(
                f"{len(conflicts)} time conflict(s) found. See the warnings above."
            )
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
