from bopytex.tasks import Task


def simple(options: dict) -> list[Task]:
    """Simple planner with options['quantity'] tasks and no dependencies"""
    return [
        Task("DO", args={"number": i}, deps=[], output=f"{i}")
        for i in range(options["quantity"])
    ]
