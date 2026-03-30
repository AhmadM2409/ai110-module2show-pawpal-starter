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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
