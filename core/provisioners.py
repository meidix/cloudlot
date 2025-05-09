import typing
import math

from .resources import ProcessingResource, MemoryResource
from .task import Task


class ResourceProvisioner:

    def __init__(self, cpus: typing.List[ProcessingResource], memory: MemoryResource, over_provisioning_factor: float):
        self.cpus = cpus
        self.memory = memory
        self.over_provisioning_factor = over_provisioning_factor
        self._cpu_request_map = {}
        self.current_index = 0
        self.task_map: typing.Dict[str, typing.List[Task]] = {}

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

    def provision(self,  entity_uid: str, cpu_power: int) -> bool:
        currently_provisioned = sum(self._cpu_request_map.values())
        if currently_provisioned + cpu_power > self.over_provisioning_factor * self.get_total_cpu_capacity():
            return False
        self._cpu_request_map[entity_uid] = cpu_power
        return True

    def _add_to_task_map(self, task: Task):
        if task.uid not in self.task_map:
            self.task_map[task.uid] = [task]
        else:
            self.task_map[task.uid].append(task)

    def allocate(self, task: Task) -> bool:
        allocated = self._allocate(task)
        if allocated:
            self._add_to_task_map(task)
            return True
        return False

    def _allocate(self, task: Task) -> bool:
        cpu_limitation = self._cpu_request_map.get(task.uid, None)
        if cpu_limitation is None:
            raise Exception("CPU not provisioned")

        allocating_amount = min(task.remaining_mi, cpu_limitation)
        allocated_amount = self._allocate_cpu(task, task.cpu_count, allocating_amount)
        if allocated_amount > 0:
            task.set_cpu(allocated_amount)
            return self.memory.allocate(task, task.mem_request)
        return False

    def _allocate_cpu(self, task, cpu_count: int, requested_power: int) -> int:
        core_power = math.ceil(requested_power / cpu_count)
        cpu_indices = []
        total_allocated = 0
        retry = len(self.cpus)
        while len(cpu_indices) < cpu_count and retry >= 0:
            cpu = self.cpus[self.current_index]
            cpu_indices.append(self.current_index)
            self.current_index = (self.current_index + 1) % len(self.cpus)
            retry -= 1

        for index in cpu_indices:
            total_allocated += self.cpus[index].allocate(task, core_power)
        return total_allocated

    def get_cpu_utilization(self):
        utilization_sum = 0
        for cpu in self.cpus:
            utilization_sum += cpu.get_utilization()
        return round(utilization_sum / len(self.cpus), 5)
