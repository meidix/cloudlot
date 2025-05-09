from core.resources import ProcessingResource

class TestProcessingResourceAllocation:

    def test_single_task_is_well_allocated(self):
        cpu = ProcessingResource(4000)
        allocated = cpu.allocate("test1", 3000)
        assert allocated == 3000
        assert cpu.get_utilization() == 0.75

    def test_two_tasks_co_located_peacefully(self):
        cpu = ProcessingResource(4000)
        allocated = cpu.allocate("test1", 2000)
        assert allocated == 2000

        allocated = cpu.allocate("test2", 2000)
        assert allocated == 2000

        assert cpu.get_utilization() == 1.0

    def test_task_co_location_causes_redistribution(self):
        cpu = ProcessingResource(4000)
        allocated = cpu.allocate("test1", 3000)
        assert allocated == 3000
        allocated = cpu.allocate("test2", 3000)
        assert allocated == 2000

        assert len(cpu.starving) == 2
        assert cpu.get_utilization() == 1.0

    def test_task_finishing_causes_expansion(self):
        cpu = ProcessingResource(4000)
        allocated = cpu.allocate("test1", 3000)
        assert allocated == 3000
        allocated = cpu.allocate("test2", 3000)
        assert allocated == 2000

        cpu.deallocate("test1")
        assert cpu.get_utilization() == 0.75




