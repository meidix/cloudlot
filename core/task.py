class Task:

    def __init__(self, uid, cpu_count, cpu_request, mem_request):
        self.uid = uid
        self.cpu_count = cpu_count
        self.request_mi = cpu_request
        self.remaining_mi = cpu_request
        self.mem_request = mem_request


class ExecutableMixin:

    def to_task(self) -> Task:
        return Task(
            self.uid,
            self.cores,
            self.length,
            self.ram
        )