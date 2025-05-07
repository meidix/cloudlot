import pytest

from serverless.client import Client
from serverless.request import ServerlessRequest
from serverless.scheduler import Scheduler
from core.identities import IDPool
from core.simulator import Simulator


@pytest.fixture
def simulator():
    return Simulator("Test", 2500)


@pytest.fixture
def serverless_request():
    return ServerlessRequest(
        IDPool.new_id(ServerlessRequest), 1.00, 1, 1, 1, 1, 128
    )


@pytest.fixture
def simulator_full(simulator, serverless_request):
    client = Client([serverless_request])
    scheduler = Scheduler()
    simulator.register(client)
    simulator.register(scheduler)
    return simulator
