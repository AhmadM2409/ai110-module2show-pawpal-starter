import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import time
import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_task(description="Feed", time_str="09:00", duration=30, priority=2, category="Feeding"):
    return Task(
        description=description,
        time=time_str,
        duration=duration,
        priority=priority,
        category=category,
    )


# ── Task tests ───────────────────────────────────────────────────────────────

class TestTask:

    def test_mark_complete_flips_status(self):
        task = make_task()
        assert task.is_completed is False
        task.mark_complete()
        assert task.is_completed is True

    def test_mark_complete_is_idempotent(self):
        task = make_task()
        task.mark_complete()
        task.mark_complete()   # calling twice should not raise or revert
        assert task.is_completed is True


# ── Pet tests ────────────────────────────────────────────────────────────────

class TestPet:

    def test_add_task_appends_to_list(self):
        pet = Pet(name="Buddy", species="Dog")
        task = make_task()
        pet.add_task(task)
        assert task in pet.tasks
        assert len(pet.tasks) == 1

    def test_add_task_stamps_pet_name(self):
        pet = Pet(name="Buddy", species="Dog")
        task = make_task()
        pet.add_task(task)
        assert task.pet_name == "Buddy"

    def test_add_multiple_tasks(self):
        pet = Pet(name="Misty", species="Cat")
        pet.add_task(make_task("Task A"))
        pet.add_task(make_task("Task B"))
        assert len(pet.tasks) == 2


# ── Scheduler conflict detection tests ───────────────────────────────────────

class TestSchedulerConflicts:

    def _build_owner_with_overlap(self):
        """Buddy has two overlapping tasks; Misty has none."""
        buddy = Pet(name="Buddy", species="Dog")
        buddy.add_task(make_task("Morning walk",  time_str="08:00", duration=30))
        buddy.add_task(make_task("Flea treatment", time_str="08:15", duration=20))

        misty = Pet(name="Misty", species="Cat")
        misty.add_task(make_task("Vet medication", time_str="09:00", duration=10))

        owner = Owner(name="Alex")
        owner.add_pet(buddy)
        owner.add_pet(misty)
        return owner

    def test_detects_exactly_one_conflict(self):
        owner = self._build_owner_with_overlap()
        scheduler = Scheduler()
        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
        assert len(conflicts) == 1

    def test_conflict_involves_correct_pet(self):
        owner = self._build_owner_with_overlap()
        scheduler = Scheduler()
        task_a, task_b = scheduler.detect_conflicts(owner.get_all_tasks())[0]
        assert task_a.pet_name == "Buddy"
        assert task_b.pet_name == "Buddy"

    def test_conflict_identifies_correct_tasks(self):
        owner = self._build_owner_with_overlap()
        scheduler = Scheduler()
        task_a, task_b = scheduler.detect_conflicts(owner.get_all_tasks())[0]
        descriptions = {task_a.description, task_b.description}
        assert descriptions == {"Morning walk", "Flea treatment"}

    def test_no_conflict_when_tasks_are_sequential(self):
        pet = Pet(name="Buddy", species="Dog")
        pet.add_task(make_task("Walk",    time_str="08:00", duration=30))
        pet.add_task(make_task("Feeding", time_str="08:30", duration=15))  # starts exactly when walk ends

        owner = Owner(name="Alex")
        owner.add_pet(pet)
        scheduler = Scheduler()
        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
        assert len(conflicts) == 0

    def test_cross_pet_tasks_never_conflict(self):
        buddy = Pet(name="Buddy", species="Dog")
        misty = Pet(name="Misty", species="Cat")
        buddy.add_task(make_task("Walk",     time_str="09:00", duration=60))
        misty.add_task(make_task("Grooming", time_str="09:15", duration=30))  # same slot, different pet

        owner = Owner(name="Alex")
        owner.add_pet(buddy)
        owner.add_pet(misty)
        scheduler = Scheduler()
        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
        assert len(conflicts) == 0
