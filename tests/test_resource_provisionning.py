from core.task import Task
from core.provisioners import ResourceProvisioner
from core.resources import Resource


class TestResourceProvisioning:

    def set_up(self):
        self.task = Task("Container#1", 1, 2500, 256)
        self.cpus = [Resource(5000) for i in range(8)]
        self.memory = Resource(31298)
        self.provisioner = ResourceProvisioner(self.cpus, self.memory)

    def test_single_task_allocation_works(self):
        self.set_up()
        self.provisioner.provision(self.task.uid, 4000)
        result = self.provisioner.allocate(self.task)
        assert result is True
        assert self.provisioner.get_cpu_utilization() == 0.0625

    def test_one_task_needs_more_than_a_single_core(self):
        self.set_up()
        big_task = Task("Container#2", 1, 4500, 256)
        self.provisioner.provision(big_task.uid, 4000)
        result = self.provisioner.allocate(big_task)
        assert result is True
        assert self.provisioner.get_cpu_utilization() == 0.1

    def test_one_task_occupying_multiple_cores(self):
        self.set_up()
        task = Task("Container#2", 2, 7412, 512)
        self.provisioner.provision("Container#2", 7500)
        result = self.provisioner.allocate(task)
        assert result is True
        assert self.provisioner.get_cpu_utilization() == 0.1853
        assert self.provisioner.cpus[0].get_utilization() == 0.7412
        assert self.provisioner.cpus[1].get_utilization() == 0.7412

    def test_multiple_tasks_fill_up_cpu(self):
        self.set_up()
        task = Task("Container#2", 2, 8000, 1024)
        self.provisioner.provision("Container#2", 8000)
        result = self.provisioner.allocate(task)
        assert result is True

        task = Task("Container#3", 1, 4000, 256)
        self.provisioner.provision("Container#3", 4000)
        result = self.provisioner.allocate(task)
        assert result is True

        task = Task("Container#4", 2, 9000, 3192)
        self.provisioner.provision("Container#4", 10000)
        result = self.provisioner.allocate(task)
        assert result is True

        task = Task("Container#5", 2, 9000, 3192)
        self.provisioner.provision("Container#5", 10000)
        result = self.provisioner.allocate(task)
        assert result is True

        task = Task("Container#6", 1, 2000, 256)
        self.provisioner.provision("Container#6", 2000)
        result = self.provisioner.allocate(task)
        assert result is True

        assert self.provisioner.get_cpu_utilization() == 0.80


