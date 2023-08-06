""" Scheduler for action to make """


from bopytex.tasks import Task
from bopytex.worker import Dispatcher


class Scheduler:
    """Scheduler is responsible of getting tasks (the tasks) and yield those that can be done"""

    def __init__(self, dispatcher: Dispatcher, output_done: list[str] = None):
        self._dispatcher = dispatcher

        if output_done is None:
            self._output_done = []
        else:
            self._output_done = output_done

        self._tasks = []
        self._failed_tasks = []

    @property
    def tasks(self) -> list[Task]:
        """List all the tasks todo"""
        return self._tasks

    @property
    def doable_tasks(self) -> list[Task]:
        """List all doable tasks"""
        return [
            task
            for task in self.tasks
            if not task.deps or all([d in self.output_done for d in task.deps])
        ]

    @property
    def all_deps(self) -> set[str]:
        """List dependencies of all tasks"""
        return {d for task in self.tasks for d in task.deps}

    @property
    def all_output(self) -> set[str]:
        """List ouput of all tasks"""
        return {task.output for task in self.tasks}

    @property
    def output_done(self) -> list[str]:
        return self._output_done

    @property
    def failed_tasks(self) -> list[Task]:
        return self._failed_tasks

    def append(self, tasks: list[Task]):
        self._tasks += tasks

    def is_finishable(self):
        return self.all_deps.issubset(self.all_output)

    def next_task(self):
        try:
            task = self.doable_tasks[0]
        except IndexError:
            raise StopIteration

        self._tasks.remove(task)
        message = self._dispatcher(task)
        if message.status == 0:
            self._output_done.append(task.output)
        else:
            self._failed_tasks.append(task)

        return message

    def backlog(self):
        """Yield tasks sorted according to dependencies"""
        while self.doable_tasks:
            yield self.next_task()
