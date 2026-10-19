from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task(description="Morning walk", time=time(8, 0))
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi")
    assert len(pet.tasks) == 0

    pet.add_task(Task(description="Feed breakfast", time=time(7, 30)))

    assert len(pet.tasks) == 1


def make_scheduler(*pets):
    owner = Owner(name="Sam")
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner=owner)


# --- Sorting ---

def test_sort_by_time_returns_chronological_order():
    mochi = Pet(name="Mochi")
    mochi.add_task(Task(description="Dinner", time=time(18, 0)))
    mochi.add_task(Task(description="Breakfast", time=time(7, 30)))
    mochi.add_task(Task(description="Lunch", time=time(12, 15)))
    scheduler = make_scheduler(mochi)

    result = scheduler.sort_by_time()

    assert [t.description for t in result] == ["Breakfast", "Lunch", "Dinner"]


def test_sort_by_time_spans_multiple_pets_and_keeps_midnight_boundaries():
    mochi, luna = Pet(name="Mochi"), Pet(name="Luna")
    mochi.add_task(Task(description="Late snack", time=time(23, 59)))
    luna.add_task(Task(description="Midnight meds", time=time(0, 0)))
    mochi.add_task(Task(description="Walk", time=time(8, 0)))
    scheduler = make_scheduler(mochi, luna)

    result = scheduler.sort_by_time()

    assert [t.time for t in result] == [time(0, 0), time(8, 0), time(23, 59)]


def test_sort_by_time_is_stable_and_does_not_mutate_input():
    mochi = Pet(name="Mochi")
    first = Task(description="First", time=time(9, 0))
    second = Task(description="Second", time=time(9, 0))
    early = Task(description="Early", time=time(6, 0))
    for t in (first, second, early):
        mochi.add_task(t)
    scheduler = make_scheduler(mochi)
    original = list(mochi.tasks)

    result = scheduler.sort_by_time(mochi.tasks)

    assert result == [early, first, second]
    assert mochi.tasks == original


def test_sort_by_time_with_empty_list_returns_empty_not_everything():
    mochi = Pet(name="Mochi")
    mochi.add_task(Task(description="Walk", time=time(8, 0)))
    scheduler = make_scheduler(mochi)

    assert scheduler.sort_by_time([]) == []


def test_sort_with_no_pets_returns_empty_list():
    assert make_scheduler().sort_by_time() == []


# --- Recurrence ---

def test_completing_daily_task_creates_task_for_following_day():
    mochi = Pet(name="Mochi")
    walk = Task(description="Walk", time=time(8, 0), frequency="daily")
    mochi.add_task(walk)
    scheduler = make_scheduler(mochi)

    new_task = scheduler.mark_task_complete(walk)

    assert walk.completed is True
    assert new_task is not None
    assert new_task in mochi.tasks
    assert new_task.completed is False
    assert new_task.due_date == date.today() + timedelta(days=1)
    assert new_task.description == "Walk"
    assert new_task.time == time(8, 0)
    assert new_task.pet_name == "Mochi"
    assert len(mochi.tasks) == 2


def test_completing_weekly_task_creates_task_seven_days_out():
    mochi = Pet(name="Mochi")
    bath = Task(description="Bath", time=time(10, 0), frequency="weekly")
    mochi.add_task(bath)

    new_task = make_scheduler(mochi).mark_task_complete(bath)

    assert new_task.due_date == date.today() + timedelta(days=7)


def test_completing_one_off_task_does_not_create_new_task():
    mochi = Pet(name="Mochi")
    vet = Task(description="Vet visit", time=time(14, 0), frequency="once")
    mochi.add_task(vet)

    result = make_scheduler(mochi).mark_task_complete(vet)

    assert result is None
    assert vet.completed is True
    assert mochi.tasks == [vet]


def test_recurrence_attaches_to_the_correct_pet_only():
    mochi, luna = Pet(name="Mochi"), Pet(name="Luna")
    mochi.add_task(Task(description="Walk", time=time(8, 0), frequency="daily"))
    feed = Task(description="Feed", time=time(9, 0), frequency="daily")
    luna.add_task(feed)

    make_scheduler(mochi, luna).mark_task_complete(feed)

    assert len(mochi.tasks) == 1
    assert len(luna.tasks) == 2


def test_next_day_task_is_excluded_from_todays_plan():
    mochi = Pet(name="Mochi")
    walk = Task(description="Walk", time=time(8, 0), frequency="daily")
    mochi.add_task(walk)
    scheduler = make_scheduler(mochi)

    scheduler.mark_task_complete(walk)

    assert scheduler.generate_daily_plan() == []


# --- Conflict detection ---

def test_detect_conflicts_flags_duplicate_times_for_same_pet():
    mochi = Pet(name="Mochi")
    mochi.add_task(Task(description="Walk", time=time(8, 0)))
    mochi.add_task(Task(description="Brush", time=time(8, 0)))

    warnings = make_scheduler(mochi).detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Walk" in warnings[0] and "Brush" in warnings[0]


def test_detect_conflicts_flags_duplicate_times_across_pets():
    mochi, luna = Pet(name="Mochi"), Pet(name="Luna")
    mochi.add_task(Task(description="Walk", time=time(8, 0)))
    luna.add_task(Task(description="Feed", time=time(8, 0)))

    warnings = make_scheduler(mochi, luna).detect_conflicts()

    assert len(warnings) == 1
    assert "Mochi" in warnings[0] and "Luna" in warnings[0]


def test_detect_conflicts_returns_empty_when_times_differ():
    mochi = Pet(name="Mochi")
    mochi.add_task(Task(description="Walk", time=time(8, 0)))
    mochi.add_task(Task(description="Brush", time=time(8, 1)))

    assert make_scheduler(mochi).detect_conflicts() == []


def test_detect_conflicts_ignores_same_time_on_different_dates():
    mochi = Pet(name="Mochi")
    today = Task(description="Walk", time=time(8, 0))
    tomorrow = Task(
        description="Walk",
        time=time(8, 0),
        due_date=date.today() + timedelta(days=1),
    )
    mochi.add_task(today)
    mochi.add_task(tomorrow)

    assert make_scheduler(mochi).detect_conflicts() == []


def test_detect_conflicts_ignores_completed_tasks():
    mochi = Pet(name="Mochi")
    walk = Task(description="Walk", time=time(8, 0))
    mochi.add_task(walk)
    mochi.add_task(Task(description="Brush", time=time(8, 0)))
    scheduler = make_scheduler(mochi)
    assert len(scheduler.detect_conflicts()) == 1

    walk.mark_complete()

    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_with_no_tasks_returns_empty_list():
    assert make_scheduler(Pet(name="Mochi")).detect_conflicts() == []


# --- Filtering ---

def test_filter_tasks_by_completion_and_pet():
    mochi, luna = Pet(name="Mochi"), Pet(name="Luna")
    done = Task(description="Walk", time=time(8, 0))
    pending = Task(description="Brush", time=time(9, 0))
    other = Task(description="Feed", time=time(10, 0))
    mochi.add_task(done)
    mochi.add_task(pending)
    luna.add_task(other)
    done.mark_complete()
    scheduler = make_scheduler(mochi, luna)

    assert scheduler.filter_tasks(completed=True) == [done]
    assert scheduler.filter_tasks(completed=False) == [pending, other]
    assert scheduler.filter_tasks(pet_name="Mochi") == [done, pending]
    assert scheduler.filter_tasks(completed=False, pet_name="Mochi") == [pending]
    assert scheduler.filter_tasks(pet_name="Nobody") == []


# --- Known gaps: these are expected to FAIL until the code is fixed ---

def test_next_occurrence_of_overdue_task_is_never_in_the_past():
    mochi = Pet(name="Mochi")
    due = date.today() - timedelta(days=3)
    walk = Task(description="Walk", time=time(8, 0), frequency="daily", due_date=due)
    mochi.add_task(walk)

    new_task = make_scheduler(mochi).mark_task_complete(walk)

    assert new_task.due_date == date.today() + timedelta(days=1)


def test_next_occurrence_is_based_on_due_date_when_completed_early():
    mochi = Pet(name="Mochi")
    due = date.today() + timedelta(days=5)
    bath = Task(description="Bath", time=time(10, 0), frequency="weekly", due_date=due)
    mochi.add_task(bath)

    new_task = make_scheduler(mochi).mark_task_complete(bath)

    assert new_task.due_date == due + timedelta(days=7)


def test_completing_same_task_twice_does_not_create_duplicate_successors():
    mochi = Pet(name="Mochi")
    walk = Task(description="Walk", time=time(8, 0), frequency="daily")
    mochi.add_task(walk)
    scheduler = make_scheduler(mochi)

    first = scheduler.mark_task_complete(walk)
    second = scheduler.mark_task_complete(walk)

    assert first is not None
    assert second is None
    assert len(mochi.tasks) == 2


def test_filter_tasks_includes_task_appended_directly_to_pet():
    mochi = Pet(name="Mochi")
    mochi.tasks.append(Task(description="Walk", time=time(8, 0)))  # bypasses add_task
    scheduler = make_scheduler(mochi)

    result = scheduler.filter_tasks(pet_name="Mochi")

    assert [t.description for t in result] == ["Walk"]
