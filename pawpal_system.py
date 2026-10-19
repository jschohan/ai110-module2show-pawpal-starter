from dataclasses import dataclass, field
from datetime import date, time, timedelta
from typing import List, Optional


@dataclass
class Task:
    """A single pet-care activity."""
    description: str
    time: time
    frequency: str = "once"  # e.g. "once", "daily", "weekly"
    completed: bool = False
    pet_name: str = ""  # set by Pet.add_task
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False

    def next_occurrence(self) -> Optional["Task"]:
        """Build the next occurrence of a recurring task.

        Returns a new, incomplete Task with the same description, time and
        frequency, due today + 1 day ("daily") or today + 7 days ("weekly").
        Returns None for any other frequency (e.g. "once"). The new task is
        not attached to a pet; Scheduler.mark_task_complete does that.
        """
        days = {"daily": 1, "weekly": 7}.get(self.frequency)
        if days is None:
            return None
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            due_date=date.today() + timedelta(days=days),
        )


@dataclass
class Pet:
    """A pet and the tasks assigned to it."""
    name: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Owner:
    """An owner who manages multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every pet's tasks together in one list."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    """The brain: retrieves, organizes, and manages tasks across all pets."""
    owner: Owner

    def get_all_tasks(self) -> List[Task]:
        # Always read through the Owner so every pet is included.
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.get_all_tasks() if not t.completed]

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and schedule its next occurrence if it recurs.

        For "daily" and "weekly" tasks, the next occurrence (see
        Task.next_occurrence) is added to the same pet that owns `task`.
        Returns the new task, or None if the task doesn't recur or no pet
        owns it. Call this instead of Task.mark_complete() to get recurrence.
        """
        task.mark_complete()
        nxt = task.next_occurrence()
        if nxt is not None:
            pet = next((p for p in self.owner.pets if task in p.tasks), None)
            if pet is not None:
                pet.add_task(nxt)
        return nxt

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks ordered by time of day, earliest first.

        Sorts `tasks` if given, otherwise every task across all pets. Returns
        a new list and leaves the input unchanged. Ties keep their original
        order (stable sort). Sorts on time only, not due_date.
        """
        if tasks is None:
            tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks belonging to the pet with this name (any status)."""
        return [
            task
            for pet in self.owner.pets
            if pet.name == pet_name
            for task in pet.tasks
        ]

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter all tasks by completion status and/or pet name.

        Args:
            completed: True for finished tasks, False for pending ones,
                None to ignore completion status.
            pet_name: Keep only this pet's tasks, or None to include all pets.

        Returns tasks in storage order (use sort_by_time to order them). When
        both criteria are given, a task must match both.
        """
        tasks = self.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Find pending tasks scheduled at the same date and time.

        Groups pending tasks by (due_date, time); every slot holding more than
        one task, for the same pet or different pets, yields one warning
        string naming the clashing tasks. Completed tasks are ignored.
        Returns an empty list when there are no conflicts and never raises.
        Only exact start-time matches are detected; tasks have no duration,
        so partial overlaps are not caught. Runs in O(n).
        """
        slots: dict = {}
        for t in self.get_pending_tasks():
            slots.setdefault((t.due_date, t.time), []).append(t)
        return [
            f"Warning: {len(group)} tasks at {when:%H:%M} on {day}: "
            + ", ".join(f"{t.pet_name} - {t.description}" for t in group)
            for (day, when), group in slots.items()
            if len(group) > 1
        ]

    def generate_daily_plan(self) -> List[Task]:
        """Return today's plan: pending tasks due today or earlier, by time.

        Future-dated tasks (e.g. the next occurrence of a daily task) are
        excluded until their due date arrives.
        """
        today = date.today()
        due = [t for t in self.get_pending_tasks() if t.due_date <= today]
        return self.sort_by_time(due)
