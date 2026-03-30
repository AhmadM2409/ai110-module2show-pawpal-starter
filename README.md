# PawPal+ — Smart Pet Care Scheduler

PawPal+ is an intelligent daily planner for pet owners. Add your pets, assign care tasks with priorities and schedules, and let the built-in scheduler build an optimized, conflict-free day — automatically rescheduling recurring tasks so nothing gets missed.

---

## Key Features

### Three-Key Smart Sorting
The scheduler orders your day using a three-level priority system:

1. **Completion status** — pending tasks always surface above completed ones
2. **Priority (1–3)** — high-priority items lead the list
3. **Chronological time** — ties broken by start time for a clean daily flow

### Conflict Detection
The scheduler scans every pet's task list for time overlaps using interval arithmetic (`start_time + duration`). Conflicts are flagged as persistent warnings at the top of the dashboard — visible at a glance without needing to generate a plan first.

### Recurring Task Cloning
Tasks can be marked `Once`, `Daily`, or `Weekly`. When a recurring task is completed, the system automatically clones it with the next scheduled date and re-adds it to the pet's list — keeping the schedule perpetually up to date without manual re-entry.

### Pending / Completed Toggle
A sidebar radio switch filters the entire dashboard — task tables, expander counts, and the generated plan — between **Pending** and **Completed** views instantly.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| UI Framework | Streamlit |
| Testing | pytest |
| Core Logic | Python `dataclasses`, `datetime`, `timedelta` |

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone <repo-url>
cd ai110-module2show-pawpal-starter
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Testing

The automated test suite covers task completion, pet–task wiring, conflict detection, and boundary conditions (sequential tasks, cross-pet overlaps).

```bash
python -m pytest tests/ -v
```

Expected output:
```
10 passed in 0.03s
```

---

## Project Structure

```
ai110-module2show-pawpal-starter/
├── app.py               # Streamlit UI — all pages and forms
├── pawpal_system.py     # Core logic — Task, Pet, Owner, Scheduler dataclasses
├── requirements.txt     # streamlit, pytest
├── reflection.md        # Design decisions, tradeoffs, and AI collaboration notes
└── tests/
    └── test_pawpal.py   # 10 pytest tests covering core logic
```

---

## System Design

```
Owner
 └── Pet (1 or more)
      └── Task (1 or more)
           ├── mark_complete(pet)  →  clones self if Daily/Weekly
           └── pet_name            →  stamped by Pet.add_task()

Scheduler
 ├── generate_daily_plan(owner, include_completed)
 ├── sort_tasks_by_priority(tasks)    →  (is_completed, priority, time)
 ├── filter_tasks(tasks, show_completed)
 └── detect_conflicts(tasks)          →  interval overlap per pet
```

---

## Design Tradeoffs

**Conflict detection uses exact overlap** — a task is flagged if it starts before another ends. Buffer time between tasks is not modelled, which is a deliberate simplification: for a single-home domestic scenario, travel time between tasks is negligible and the added complexity would not benefit the target user.

**In-memory storage via `st.session_state`** — all data lives in the browser session. This is appropriate for a lab prototype but would require SQLite or a similar persistence layer for a production app where users need data across sessions.

---

*Built for AI110 — Module 2 Lab Assignment*
