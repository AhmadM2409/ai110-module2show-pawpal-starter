# PawPal+ Project Reflection

## 1. System Design

**Core User Actions:**
1. **Profile Management**: Entering and storing basic owner and pet profiles.
2. **Task Entry & Customization**: Adding or editing pet care tasks with specific durations, categories, and priority levels.
3. **Daily Plan Generation**: Producing an optimized daily schedule that respects time constraints and priorities.

**a. Initial design**

My initial design uses a modular, object-oriented approach with four primary classes:
* **Task (Dataclass)**: The base unit of data, holding description, time, duration, priority, and category.
* **Pet (Dataclass)**: A container for specific animal info and a list of its assigned tasks.
* **Owner**: Manages the high-level profile and coordinates multiple Pet objects.
* **Scheduler**: The logic engine that processes the Owner's tasks to handle sorting and conflict detection.

**b. Design changes**

Based on the AI architectural review, I made three key refinements to the design:
1. **Time Objects**: Changed the `Task.time` attribute from a string to `datetime.time` to ensure robust comparison and conflict detection logic.
2. **Task Context**: Added a `pet_name` field to the `Task` dataclass so that the Scheduler can identify which pet a task belongs to when tasks are flattened into a single list.
3. **Conflict Dataclass**: Replaced raw tuples in the `Scheduler` with a dedicated `Conflict` dataclass to provide clearer, more readable output for the UI.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three primary constraints in a hierarchical "Three-Key Sort":
* **Completion Status**: Completed tasks are automatically pushed to the bottom of the list to keep the "To-Do" items front and center.
* **Priority (1-3)**: Among pending tasks, high-priority items (Priority 1) are moved to the top.
* **Time**: Tasks with the same priority are sorted chronologically.

I decided that **Completion Status** was the most important constraint for user experience, as it prevents a cluttered "finished" list from burying urgent, upcoming tasks.

**b. Tradeoffs**

A key tradeoff in this design is the **"Exact Overlap"** detection. The scheduler flags a conflict if one task starts before another ends, but it does *not* account for "buffer time" or travel time between tasks. 

This is reasonable for a domestic pet care scenario where most tasks (feeding, meds) happen in the same location. Adding complex buffer logic would have increased the system's complexity without providing significant value for a single-home user.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI as a "Co-Architect" throughout the project:
* **Design Brainstorming**: Using Claude to refine the initial class structures and identify data bottlenecks.
* **Refactoring**: Leveraging AI to quickly convert string-based time logic to `datetime.time` across the entire codebase.
* **Logic Implementation**: Providing high-level pseudo-code prompts to have the AI "flesh out" method bodies for the Scheduler and recurring task logic.

**b. Judgment and verification**

During the Phase 1 review, the AI suggested a `Conflict` dataclass instead of raw tuples. I didn't blindly accept it until I realized it would make the Streamlit UI code much cleaner. I evaluated this by attempting to write the UI code both ways and found that the AI’s suggestion significantly reduced the amount of string parsing I had to do in the frontend.

---

## 4. Testing and Verification

**a. What you tested**

I implemented a suite of 10 automated tests using `pytest` covering:
* **State Management**: Ensuring `mark_complete()` toggles correctly and clones recurring tasks.
* **Logic Integrity**: Verifying that `add_task()` correctly stamps the pet's name onto the task.
* **Boundary Conditions**: Testing sequential tasks (one ending exactly when another starts) to ensure they do *not* trigger a false conflict.

**b. Confidence**

I am highly confident in the core scheduler logic because the automated test suite passes 100% of the time in under 0.05 seconds. 

If I had more time, I would test **cross-day scheduling** (e.g., a task starting at 11:30 PM and ending at 12:30 AM) and **timezone transitions**, which are common edge cases for mobile users who travel with their pets.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the **Recurring Task Logic**. Being able to mark a "Daily Feed" as complete and having the system automatically generate a fresh, pending version for the next day makes the app feel proactive rather than just a passive list.

**b. What you would improve**

If I had another iteration, I would redesign the **Task Storage**. Currently, everything lives in memory via `st.session_state`. Integrating a local SQLite database would allow users to close their browser without losing their entire pet history.

**c. Key takeaway**

The most important thing I learned is the value of **"CLI-First" development**. By building and testing the core logic in a simple terminal environment before touching the Streamlit UI, I avoided hours of debugging browser-refresh issues and could focus entirely on the "brain" of the application.