
class ResourceFullException(Exception):
    pass


class ResourceEmptyException(Exception):
    pass


class Resource:

    def __init__(self, capacity):
        self.capacity = capacity
        self.currently_allocated = 0

    @property
    def available(self):
        return self.capacity - self.currently_allocated

    def get_utilization(self):
        return self.currently_allocated / self.capacity

    def allocate(self, requested_amount) -> bool:
        if requested_amount > self.available:
            return False
        else:
            self.currently_allocated += requested_amount
            return True

    def deallocate(self, freed_amount) -> bool:
        if freed_amount > self.currently_allocated:
            return False
        self.currently_allocated -= freed_amount
        return True

