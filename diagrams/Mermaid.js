// PawPal+ — Mermaid diagram string export
// Use this in a web page that loads mermaid, or import the string for tooling.
const diagram = `
classDiagram
    class Owner {
        +string name
        +int daily_available_minutes
        +dict preferences
        +update_availability(minutes:int)
        +add_preference(key:str, value)
        +get_preferences(): dict
        +add_pet(pet:Pet)
        +remove_pet(pet_name:str)
        +get_pets(): List~Pet~
        +get_all_tasks(): List~Task~
    }

    class Pet {
        +string name
        +string species
        +int age
        +List~Task~ tasks
        +add_task(t:Task)
        +remove_task(task_name:str)
        +get_tasks(): List~Task~
        +get_tasks_by_category(category:str): List~Task~
    }

    class Task {
        +string name
        +int duration
        +int priority
        +string category
        +bool completed
        +bool must_do
        +string preferred_time
        +string frequency
        +date due_date
        +string time
        +mark_complete()
        +update_priority(new_priority:int)
        +update_duration(new_duration:int)
        +is_mandatory(): bool
    }

    class Scheduler {
        +Owner owner
        +List~Pet~ pets
        +Schedule schedule
        -List~Task~ _unscheduled
        +generate_schedule(): Schedule
        +clear_schedule()
        +get_schedule(): Schedule
        +sort_tasks_by_priority(tasks:List~Task~): List~Task~
        +sort_by_time(tasks:List~Task~, reverse:bool): List~Task~
        +filter_feasible_tasks(tasks:List~Task~, available_minutes:int): List~Task~
        +filter_tasks(completed:bool, pet_name:str): List~Task~
        +apply_preferences(tasks:List~Task~): List~Task~
        +enforce_mandatory_tasks(tasks:List~Task~): List~Task~
        +mark_task_complete(task:Task, pet_name:str): Task
        +detect_time_conflicts(tasks:List~Task~): dict
        +conflict_warnings(tasks:List~Task~): List~str~
        +explain_schedule(): dict
        +get_unscheduled_tasks(): List~Task~
        +get_total_time_used(): int
    }

    class Schedule {
        +List~Task~ tasks
        +int total_time
        +int remaining_time
        +add_task(t:Task)
        +remove_task(task_name:str)
        +calculate_total_time(): int
        +summarize(): string
    }

    %% Associations
    Owner "1" o-- "0..*" Pet : owns
    Pet "1" o-- "0..*" Task : has
    Scheduler "1" --> "1" Owner
    Scheduler "1" --> "0..*" Pet
    Scheduler "1" o-- "0..1" Schedule : creates
    Schedule "1" o-- "0..*" Task : references
    Scheduler ..> Task : <<creates>> on recurrence
`;

export default diagram;
