import typing
import math

from .resources import Resource
from .task import Task



class ResourceProvisioner:

    def __init__(self, cpus: typing.List[Resource], memory: Resource):
        self.cpus = cpus
        self.memory = memory
        self._cpu_request_map = {}
        self.current_index = 0

    def __repr__(self):
        return f'CPUS: {self.cpus} . MEM: {self.memory}'

    def get_total_cpu_capacity(self) -> int:
        total = 0
        for cpu in self.cpus:
            total += cpu.capacity
        return total

    def get_total_memory_capacity(self) -> int:
        return self.memory.capacity

    def get_available_memory_capacity(self) -> int:
        return self.memory.available

    def get_available_cpu_capacity(self) -> int:
        available = 0
        for cpu in self.cpus:
            available += cpu.available
        return available

    def provision(self,  entity_uid: str, cpu_power: int):
        self._cpu_request_map[entity_uid] = cpu_power

    def allocate(self, task: Task) -> bool:
        cpu_limitation = self._cpu_request_map.get(task.uid, None)
        if cpu_limitation is None:
            raise Exception("CPU not provisioned")

        allocating_amount = min(task.remaining_mi, cpu_limitation)
        result = self._allocate_cpu(task.cpu_count, allocating_amount)
        if result:
            return self.memory.allocate(task.mem_request)
        return False

    def _allocate_cpu(self, cpu_count: int, requested_power: int) -> bool:
        core_power = math.ceil(requested_power / cpu_count)
        cpu_indices = []
        total_allocated = 0
        retry = len(self.cpus)
        while (total_allocated < requested_power and retry >= 0):
            cpu = self.cpus[self.current_index]
            if cpu.available >= core_power:
                total_allocated += core_power
                cpu_indices.append(self.current_index)
            self.current_index = (self.current_index + 1) % len(self.cpus)
            retry -= 1
        if len(cpu_indices) != cpu_count:
            return False
        for index in cpu_indices:
            self.cpus[index].allocate(core_power)
        return True

    def get_cpu_utilization(self):
        utilization_sum = 0
        for cpu in self.cpus:
            utilization_sum += cpu.get_utilization()
        return round(utilization_sum / len(self.cpus), 5)


