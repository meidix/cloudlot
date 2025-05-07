import re
from typing import List, Dict, Optional
from . import settings
from .event_queue import EventQueue
from .entities import SimEntity, SimEvent


class Simulator(object):
    _clock: float = 0
    _instance: "Simulator"

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Simulator, cls).__new__(cls)
        return cls._instance

    def __init__(self, name: str, simulation_time: float):
        self.simulation_name = name
        self.limit = simulation_time
        self._queue = EventQueue()
        self._entities: Dict[str, List[SimEntity]] = {}
        self._entities_uid_map: Dict[str, SimEntity] = {}

    @property
    def current_time(self):
        return self._clock

    def get_entity(self, lookup: str) -> Optional[SimEntity | List[SimEntity]]:
        pattern = r"\b[A-Z][a-zA-Z0-9]*#\d+\b"
        if re.match(pattern, lookup):
            result = self._entities_uid_map.get(lookup, None)
        else:
            result = self._entities.get(lookup, None)
        if result is None:
            raise ValueError(f"Could not find an entity with lookup term {lookup}")
        return result

    def add_entity(self, entity: SimEntity):
        key = entity.entity_type
        entity._platform = self
        if key in self._entities:
            self._entities[key].append(entity)
        else:
            self._entities[key] = [entity]
        self._entities_uid_map[entity.uid] = entity

    def clock(self):
        self._clock += settings.SIMULATOR_CLOCK_STEP

    def start(self):
        for entity in self._entities:
            entity.start_entitry()

    def run(self):
        if self.current_time == self.limit:
            self.terminate_simulation()
        self.clock()
        events = self._queue.get_next(self.current_time)
        for event in events:
            destination = self.get_entity(event.destination)
            destination.process_event(event)

    def terminate_simulation(self):
        # I need to stop every entity
        for entity in self._entities:
            entity.stop_entity()

    def register(self, entity: SimEntity):
        entity._platform = self
        self.add_entity(entity)

