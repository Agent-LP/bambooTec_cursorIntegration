import os
from typing import Optional, List
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pydantic import BaseModel, Field
from enum import Enum

console = Console()

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    category: str = Field(default="General")
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: Optional[datetime] = None
    dependencies: List[int] = Field(default_factory=list)

class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: str, category: str = "General",
                priority: Priority = Priority.MEDIUM, due_date: Optional[datetime] = None,
                dependencies: List[int] = None) -> Task:
        if dependencies is None:
            dependencies = []
            
        # Verify dependencies exist
        for dep_id in dependencies:
            if not any(task.id == dep_id for task in self.tasks):
                raise ValueError(f"Dependency task {dep_id} does not exist")
                
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            due_date=due_date,
            dependencies=dependencies
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def complete_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                # Check if all dependencies are completed
                for dep_id in task.dependencies:
                    dep_task = next((t for t in self.tasks if t.id == dep_id), None)
                    if dep_task and not dep_task.completed:
                        raise ValueError(f"Cannot complete task {task_id}: dependency {dep_id} is not completed")
                task.completed = True
                return task
        return None

    def list_tasks(self, category: Optional[str] = None, priority: Optional[Priority] = None) -> None:
        table = Table(title="Tasks")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Category", style="blue")
        table.add_column("Priority", style="red")
        table.add_column("Due Date", style="yellow")
        table.add_column("Dependencies", style="green")
        table.add_column("Status", style="yellow")

        filtered_tasks = self.tasks
        if category:
            filtered_tasks = [t for t in filtered_tasks if t.category == category]
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]

        for task in filtered_tasks:
            status = "✅" if task.completed else "❌"
            due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else "No due date"
            deps = ", ".join(map(str, task.dependencies)) if task.dependencies else "None"
            
            table.add_row(
                str(task.id),
                task.title,
                task.category,
                task.priority.value,
                due_date,
                deps,
                status
            )

        console.print(table)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def get_tasks_by_category(self, category: str) -> List[Task]:
        return [task for task in self.tasks if task.category == category]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        return [task for task in self.tasks if task.priority == priority]

def main():
    task_manager = TaskManager()
    
    while True:
        console.print(Panel.fit("Task Manager", style="bold blue"))
        console.print("1. Add Task")
        console.print("2. Complete Task")
        console.print("3. List Tasks")
        console.print("4. Filter Tasks by Category")
        console.print("5. Filter Tasks by Priority")
        console.print("6. Exit")
        
        choice = console.input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            title = console.input("Enter task title: ")
            description = console.input("Enter task description: ")
            category = console.input("Enter task category (default: General): ") or "General"
            
            console.print("\nPriority levels:")
            for i, priority in enumerate(Priority, 1):
                console.print(f"{i}. {priority.value}")
            priority_choice = int(console.input("Select priority (1-4): ")) - 1
            priority = list(Priority)[priority_choice]
            
            due_date_str = console.input("Enter due date (YYYY-MM-DD) or leave empty: ")
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
            
            deps_str = console.input("Enter dependency task IDs (comma-separated) or leave empty: ")
            dependencies = [int(dep.strip()) for dep in deps_str.split(",")] if deps_str else []
            
            try:
                task = task_manager.add_task(
                    title=title,
                    description=description,
                    category=category,
                    priority=priority,
                    due_date=due_date,
                    dependencies=dependencies
                )
                console.print(f"[green]Task {task.id} added successfully![/green]")
            except ValueError as e:
                console.print(f"[red]Error: {str(e)}[/red]")
        
        elif choice == "2":
            task_id = int(console.input("Enter task ID to complete: "))
            try:
                task = task_manager.complete_task(task_id)
                if task:
                    console.print(f"[green]Task {task.id} marked as completed![/green]")
                else:
                    console.print("[red]Task not found![/red]")
            except ValueError as e:
                console.print(f"[red]Error: {str(e)}[/red]")
        
        elif choice == "3":
            task_manager.list_tasks()
        
        elif choice == "4":
            category = console.input("Enter category to filter: ")
            task_manager.list_tasks(category=category)
        
        elif choice == "5":
            console.print("\nPriority levels:")
            for i, priority in enumerate(Priority, 1):
                console.print(f"{i}. {priority.value}")
            priority_choice = int(console.input("Select priority to filter (1-4): ")) - 1
            priority = list(Priority)[priority_choice]
            task_manager.list_tasks(priority=priority)
        
        elif choice == "6":
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        else:
            console.print("[red]Invalid choice![/red]")
        
        console.print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main() 