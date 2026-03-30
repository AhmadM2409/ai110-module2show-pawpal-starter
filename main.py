from datetime import time
from pawpal_system import Task, Pet, Owner, Scheduler

# ── Build the owner ──────────────────────────────────────────────────────────
alex = Owner(name="Alex")

buddy = Pet(name="Buddy", species="Dog")
misty = Pet(name="Misty", species="Cat")

# ── Buddy's tasks ────────────────────────────────────────────────────────────
buddy.add_task(Task(
    description="Morning walk",
    time="08:00",
    duration=30,
    priority=1,
    category="Exercise",
))

buddy.add_task(Task(
    description="Flea treatment",
    time="08:15",          # ⚠ Intentional conflict: starts while walk is still running
    duration=20,
    priority=2,
    category="Health",
))

buddy.add_task(Task(
    description="Evening feeding",
    time="18:00",
    duration=15,
    priority=1,
    category="Feeding",
))

# ── Misty's tasks ────────────────────────────────────────────────────────────
misty.add_task(Task(
    description="Playtime",
    time="10:00",
    duration=20,
    priority=3,
    category="Exercise",
))

misty.add_task(Task(
    description="Vet medication",
    time="09:00",
    duration=10,
    priority=1,
    category="Health",
))

# ── Wire everything together ─────────────────────────────────────────────────
alex.add_pet(buddy)
alex.add_pet(misty)

scheduler = Scheduler()

# ── Print today's schedule ───────────────────────────────────────────────────
print("=" * 52)
print("         TODAY'S SCHEDULE  --  Owner: Alex")
print("=" * 52)

plan = scheduler.generate_daily_plan(alex)

for task in plan:
    status = "X" if task.is_completed else "o"
    print(
        f"  [{status}] {task.time}  |  P{task.priority}  |  "
        f"{task.pet_name:<6}  |  {task.description}  "
        f"({task.duration} min, {task.category})"
    )

print("=" * 52)

# ── Print conflict report ────────────────────────────────────────────────────
all_tasks = alex.get_all_tasks()
conflicts = scheduler.detect_conflicts(all_tasks)

print()
if conflicts:
    print(f"!!  CONFLICTS DETECTED ({len(conflicts)} found)")
    print("-" * 52)
    for task_a, task_b in conflicts:
        print(f"  Pet    : {task_a.pet_name}")
        print(f"  Task A : '{task_a.description}' at {task_a.time} for {task_a.duration} min")
        print(f"  Task B : '{task_b.description}' at {task_b.time} for {task_b.duration} min")
        print("-" * 52)
else:
    print("OK  No scheduling conflicts found.")
