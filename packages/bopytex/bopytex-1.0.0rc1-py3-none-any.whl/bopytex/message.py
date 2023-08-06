class Message:
    def __init__(self, status, out, err):
        self._status = status
        self._out = out
        self._err = err

    @property
    def status(self):
        return self._status

    @property
    def out(self):
        return self._out

    @property
    def err(self):
        return self._err

    def __repr__(self):
        return f"Message(status={self.status}, out={self.out}, err={self.err})"


class SubprocessMessage(Message):
    def __init__(self, process):
        self._process = process

    @property
    def status(self):
        return self._process.wait()

    @property
    def out(self):
        return self._process.stdout

    @property
    def err(self):
        return self._process.stderr
