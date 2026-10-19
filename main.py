from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import time


def print_plan(owner_name, tasks):
    """Print a column-aligned daily plan; tasks should already be sorted by time."""
    width = 56
    print("=" * width)
    print(f"  🐾 PawPal+ Daily Plan for {owner_name}")
    print("=" * width)
    print(f"  {'TIME':<8} {'PET':<7} {'TASK':<16} {'FREQ':<7} STATUS")
    print("-" * width)
    for t in tasks:
        mark = "[x]" if t.completed else "[ ]"
        print(
            f"  {t.time:%H:%M}    {t.pet_name:<7} "
            f"{t.description:<16} {t.frequency:<7} {mark}"
        )
    print("-" * width)
    done = sum(t.completed for t in tasks)
    print(f"  {len(tasks)} tasks · {done} completed")


jim = Owner("Jim")
tom = Pet("Tom")
jerry = Pet("Jerry")
jim.add_pet(tom)
jim.add_pet(jerry)
# Tasks are added deliberately out of time order.
exercise_tom = Task("Exercise", time(14, 0), "daily")
tom.add_task(exercise_tom)
jerry_toy = Task("Give Jerry toy", time(10, 0))
jerry.add_task(jerry_toy)
feed_tom = Task("Feed", time(9, 0), "daily")
tom.add_task(feed_tom)
wash_tom = Task("Wash", time(12, 0), "weekly")
tom.add_task(wash_tom)
water_jerry = Task("Give water", time(8, 0))
jerry.add_task(water_jerry)
feed_jerry = Task("Feed", time(9, 0), "daily")
jerry.add_task(feed_jerry)

# Mark a couple complete so the completion filter has something to show.
water_jerry.mark_complete()
feed_tom.mark_complete()

planner = Scheduler(jim)


def section(title, tasks):
    print(f"\n>>> {title}")
    print_plan(jim.name, tasks)


section("Insertion order (unsorted)", planner.get_all_tasks())
section("sort_by_time()", planner.sort_by_time())
section("filter_tasks(completed=False), sorted",
        planner.sort_by_time(planner.filter_tasks(completed=False)))
section("filter_tasks(completed=True), sorted",
        planner.sort_by_time(planner.filter_tasks(completed=True)))
section("filter_tasks(pet_name='Tom'), sorted",
        planner.sort_by_time(planner.filter_tasks(pet_name="Tom")))
section("filter_tasks(completed=False, pet_name='Jerry'), sorted",
        planner.sort_by_time(planner.filter_tasks(completed=False, pet_name="Jerry")))
section("generate_daily_plan()", planner.generate_daily_plan())

# Recurrence: completing a daily/weekly task spawns the next occurrence.
print("\n>>> Recurrence via mark_task_complete()")
for task in (feed_jerry, wash_tom, jerry_toy):
    nxt = planner.mark_task_complete(task)
    if nxt:
        print(f"  Completed {task.pet_name}'s {task.description} ({task.frequency}) "
              f"-> next due {nxt.due_date}")
    else:
        print(f"  Completed {task.pet_name}'s {task.description} ({task.frequency}) "
              f"-> no recurrence")
print(f"  Tasks now: {len(planner.get_all_tasks())}")
print("  Pending tasks with due dates:")
for t in planner.sort_by_time(planner.filter_tasks(completed=False)):
    print(f"    {t.due_date}  {t.time:%H:%M}  {t.pet_name:<6} {t.description} ({t.frequency})")

# Conflict detection returns warnings instead of raising.
print("\n>>> Conflict detection")
print("  Before adding clashes:", planner.detect_conflicts() or "none")
jerry.add_task(Task("Vet call", time(14, 0)))   # same time as Tom's Exercise
for warning in planner.detect_conflicts():
    print(" ", warning)
