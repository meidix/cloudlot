class Task:

    def __init__(self, uid, cpu_count, cpu_request, mem_request):
        self.uid = uid
        self.cpu_count = cpu_count
        self.request_mi = cpu_request
        self.remaining_mi = cpu_request
        self.allocated_mi = 0
        self.mem_request = mem_request

    def __repr__(self):
        return f"Task({self.uid}, {self.cpu_count}, {self.request_mi}, {self.remaining_mi})"

    def set_cpu(self, mi):
        self.allocated_mi = mi


class ExecutableMixin:

    def to_task(self) -> Task:
        return Task(
            self.uid,
            self.cores,
            self.length,
            self.ram
        )