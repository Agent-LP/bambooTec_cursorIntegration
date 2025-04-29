from datetime import datetime
from src.main import Task, TaskManager, Priority

def test_task_creation():
    task = Task(
        id=1,
        title="Test Task",
        description="Test Description",
        category="Work",
        priority=Priority.HIGH,
        due_date=datetime(2024, 12, 31),
        dependencies=[2, 3]
    )
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.category == "Work"
    assert task.priority == Priority.HIGH
    assert task.due_date == datetime(2024, 12, 31)
    assert task.dependencies == [2, 3]
    assert not task.completed

def test_task_manager():
    manager = TaskManager()
    
    # Test basic task creation
    task = manager.add_task(
        title="Test Task",
        description="Test Description",
        category="Work",
        priority=Priority.HIGH
    )
    assert task.id == 1
    assert len(manager.tasks) == 1
    assert task.category == "Work"
    assert task.priority == Priority.HIGH
    
    # Test task with dependencies
    task2 = manager.add_task(
        title="Dependent Task",
        description="Depends on task 1",
        dependencies=[1]
    )
    assert task2.id == 2
    assert task2.dependencies == [1]
    
    # Test completing task with dependencies
    try:
        manager.complete_task(2)
        assert False, "Should not be able to complete task with incomplete dependencies"
    except ValueError:
        pass
    
    # Complete the first task
    completed_task = manager.complete_task(1)
    assert completed_task is not None
    assert completed_task.completed
    
    # Now should be able to complete the dependent task
    completed_task2 = manager.complete_task(2)
    assert completed_task2 is not None
    assert completed_task2.completed

def test_task_filtering():
    manager = TaskManager()
    
    # Add tasks with different categories and priorities
    manager.add_task("Work Task", "Description", "Work", Priority.HIGH)
    manager.add_task("Personal Task", "Description", "Personal", Priority.LOW)
    manager.add_task("Work Task 2", "Description", "Work", Priority.MEDIUM)
    
    # Test filtering by category
    work_tasks = manager.get_tasks_by_category("Work")
    assert len(work_tasks) == 2
    assert all(task.category == "Work" for task in work_tasks)
    
    # Test filtering by priority
    high_priority_tasks = manager.get_tasks_by_priority(Priority.HIGH)
    assert len(high_priority_tasks) == 1
    assert all(task.priority == Priority.HIGH for task in high_priority_tasks) 