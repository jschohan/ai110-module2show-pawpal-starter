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
feed_tom = Task("Feed", time(9, 0), "daily")
tom.add_task(feed_tom)
wash_tom = Task("Wash", time(12, 0), "weekly")
tom.add_task(wash_tom)
exercise_tom = Task("Exercise", time(14, 0), "daily")
tom.add_task(exercise_tom)
water_jerry = Task("Give water", time(8, 0))
jerry.add_task(water_jerry)
jerry_toy = Task("Give Jerry toy", time(10, 0))
jerry.add_task(jerry_toy)
feed_jerry = Task("Feed", time(9, 0), "daily")
jerry.add_task(feed_jerry)

planner = Scheduler(jim)
plan = planner.generate_daily_plan()
print_plan(jim.name, plan)
