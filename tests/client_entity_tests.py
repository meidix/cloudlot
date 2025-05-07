
class TestClientEntity:

    def test_client_start(self, simulator_full):
        simulator_full.start()
        assert len(simulator_full._queue) == 1

