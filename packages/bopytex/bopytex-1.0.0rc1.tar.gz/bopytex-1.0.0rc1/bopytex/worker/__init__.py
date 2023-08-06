class ActionNotFound(Exception):
    pass


class Dispatcher:
    def __init__(self, actions: list):
        self._actions = actions

    def __call__(self, task):
        try:
            choosen_action = self._actions[task.action]
        except KeyError:
            raise ActionNotFound(
                f"The action {task.action} is not in {self._actions.keys()}"
            )

        return choosen_action(args=task.args, deps=task.deps, output=task.output)
