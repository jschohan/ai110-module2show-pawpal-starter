from dataclasses import dataclass, field
from datetime import time
from typing import List, Optional


@dataclass
class Task:
    """A single pet-care activity."""
    description: str
    time: time
    frequency: str = "once"  # e.g. "once", "daily", "weekly"
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False


@dataclass
class Pet:
    """A pet and the tasks assigned to it."""
    name: str
    species: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
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

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        if tasks is None:
            tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        return [
            task
            for pet in self.owner.pets
            if pet.name == pet_name
            for task in pet.tasks
        ]

    def generate_daily_plan(self) -> List[Task]:
        """Pending tasks across all pets, ordered by time."""
        return self.sort_by_time(self.get_pending_tasks())
