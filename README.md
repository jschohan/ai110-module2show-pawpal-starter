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

## Implementation summary

The backend lives in [pawpal_system.py](pawpal_system.py) and is built from four small classes:

- **Task**: one care activity (description, time, frequency, completed flag). It knows which pet it belongs to via `pet_name` and can mark itself complete or incomplete.
- **Pet**: owns a list of `Task`s. `add_task` attaches a task and stamps it with the pet's name; `remove_task` detaches it.
- **Owner**: owns a list of `Pet`s and exposes `get_all_tasks()`, which flattens every pet's tasks into one list.
- **Scheduler**: the "brain." It holds an `Owner` and always reads tasks through it, so every pet is included. It can get pending tasks, sort by time, filter by pet, and `generate_daily_plan()` (pending tasks across all pets, ordered by time).

**How they fit together:** `Owner` → `Pet` → `Task` is a containment chain (an owner has pets, a pet has tasks). `Scheduler` sits on top and never stores tasks itself. It queries the owner, then sorts and filters the results, so the plan always reflects the current state of the owner's pets.

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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
--------------------------------------------------------
  08:00    Jerry   Give water       once    [ ]
  09:00    Tom     Feed             daily   [ ]
  09:00    Jerry   Feed             daily   [ ]
  10:00    Jerry   Give Jerry toy   once    [ ]
  12:00    Tom     Wash             weekly  [ ]
  14:00    Tom     Exercise         daily   [ ]
--------------------------------------------------------
  6 tasks · 0 completed

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | sort_by_time() | sorts task by pet name or time |
| Filtering | filter_tasks() | filters tasks by completion or pet names |
| Conflict handling | detect_conflicts() | detects same start time tasks |
| Recurring tasks | next_occurence() | creates a new task for reccurence |

## 📸 Demo Walkthrough

Features
Sorting by time: Tasks are ordered by time of day, earliest first. The sort is stable, so tasks at the same time keep the order they were added in. It sorts on time only, not date. The "Current tasks" table and the daily plan both use it.
Filtering by pet and status: You can narrow the task list by pet, by status (Pending or Completed), or by both at once. A task has to match both filters to show. Pet filtering reads from each pet's own task list, so it doesn't depend on a task's pet_name field.
Conflict warnings: Pending tasks are grouped by exact date and start time. Any slot holding more than one task produces a warning naming the clashing tasks and their pets. This covers clashes for the same pet and across different pets. Completed tasks are ignored, and the check is a single pass over the tasks (O(n)). The warnings appear in the UI with a suggestion to move one task. Daily and weekly recurrence: When you complete a "daily" or "weekly" task, a new task is created automatically for the same pet. It is due 1 or 7 days after the later of the original due date and today. That keeps the cadence if you finish early, and it never schedules a task in the past. One-time tasks don't repeat. Marking an already-completed task complete again does not create a duplicate.
Today's schedule: "Generate schedule" lists pending tasks due today or earlier, sorted by time. Future-dated tasks, such as tomorrow's recurrence of a daily task, stay hidden until their due date.
Multi-pet management: One owner can have several pets, each with its own tasks. The scheduler reads across all of them. The app rejects duplicate pet names, empty pet names, and empty task descriptions.
Live task summary: The app shows metrics for total, pending and completed tasks. You can toggle tasks complete or incomplete, and the table, metrics and conflict warnings refresh right away.

Describe your app in numbered steps so a reader can follow along without watching a video:
1. Type name of owner of pets
2. Type the name of pet and click add
3. Use the tasks section to select a pet then describe the task
and details pertaining to the task.
4. In the scheduler use the drop-downs to add filters to the 
daily plan that will be generated if needed. Click generate daily schedule.


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
