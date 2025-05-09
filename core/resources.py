import itertools


class ResourceFullException(Exception):
    pass


class ResourceEmptyException(Exception):
    pass


class Resource:

    def __init__(self, capacity):
        self.capacity = capacity
        self.currently_allocated = 0
        self.tasks = {}

    def __contains__(self, item):
        return item in self.tasks.keys()

    def __repr__(self):
        return f'Resource(utilization={self.get_utilization()})'

    @property
    def available(self):
        return self.capacity - self.currently_allocated

    def get_utilization(self):
        return self.currently_allocated / self.capacity

    def allocate(self, task_uid: str, requested_amount) -> int:
        if requested_amount > self.available:
            return 0
        else:
            self.currently_allocated += requested_amount
            self.tasks[task_uid] = requested_amount
            return requested_amount

    def deallocate(self, task_uid) -> bool:
        freed_amount = self.tasks[task_uid]
        self.currently_allocated -= freed_amount
        del self.tasks[task_uid]
        return True


class MemoryResource(Resource):

    def __repr__(self):
        return f'Memory(available={self.available})'


class ProcessingResource(Resource):

    def __init__(self, capacity):
        super().__init__(capacity)
        self.starving = {}

    def __repr__(self):
        return f'Processing(utilization={self.get_utilization()})'

    def allocate(self, task_uid: str, requested_amount: int) -> int:
        if requested_amount > self.available:
            new_amount = self.redistribute_power(requested_amount)
            self.starving[task_uid] = requested_amount
            return super().allocate(task_uid, new_amount)
        else:
            return super().allocate(task_uid, requested_amount)

    def redistribute_power(self, requested_amount: int) -> int:
        required_power = self.currently_allocated + requested_amount
        tasks = self.tasks.copy()
        for task_uid, allocated in tasks.items():
            new_power = int((allocated * self.capacity) / required_power)
            self.deallocate(task_uid)
            if task_uid not in self.starving:
                self.starving[task_uid] = allocated
            self.allocate(task_uid, new_power)
        return self.available

    def deallocate(self, task_uid):
        result = super().deallocate(task_uid)
        if result:
            if task_uid in self.starving:
                del self.starving[task_uid]
            new_starving_tasks = {}
            for task_uid, requested_power in self.starving.items():
                super().deallocate(task_uid)
                new_power = self.allocate(task_uid, requested_power)
                if new_power < requested_power:
                    new_starving_tasks[task_uid] = requested_power
            self.starving = new_starving_tasks
            return result



