import pytest
from core.entities import SimEntity
from core.identities import IDPool
from core.simulator import Simulator


def test_entity_lookup_by_uid():
    simulator = Simulator("Test", 2500)
    entity = SimEntity()
    entity.entity_type = 'test'
    simulator.register(entity)
    assert isinstance(simulator.get_entity(entity.uid), SimEntity)
