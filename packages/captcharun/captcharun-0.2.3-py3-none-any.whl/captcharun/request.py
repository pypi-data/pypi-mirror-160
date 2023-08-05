from captcharun.task import BaseTask


class BaseRequest:
    _path = None
    _method = "GET"
    _params = {}
    _data = {}

    @property
    def path(self):
        return self._path

    @property
    def method(self):
        return self._method

    @property
    def params(self):
        return self._params

    @property
    def data(self):
        if self.method == "GET":
            return None

        return self._data


class GetBalance(BaseRequest):
    def __init__(self, user_id: str = "self"):
        self.user_id = user_id

    @property
    def path(self):
        return f"/v2/users/{self.user_id}/wallet"


class GetTask(BaseRequest):
    def __init__(self, task_id: str):
        self.task_id = task_id

    @property
    def path(self):
        return f"/v2/tasks/{self.task_id}"


class CreateTask(BaseRequest):
    _path = "/v2/tasks"
    _method = "POST"

    def __init__(self, task: BaseTask, developer: str = None):
        self.task = task
        self.developer = developer

        self._data = dict(
            developer=self.developer,
            **self.task.data,
        )
