import re
from typing import List, Dict, Union
import settings
from .event_queue import EventQueue
from .entities import SimEntity, SimEvent


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Simulator(metaclass=Singleton):
    _clock: float = 0

    def __str__(self):
        return self.simulation_name

    def __init__(self, simulation_name: str, limit: int):
        self.simulation_name = simulation_name
        self.limit = limit
        self._queue = EventQueue()
        self._entities: Dict[str, List[SimEntity]] = {}
        self._entities_uid_map: Dict[str, SimEntity] = {}

    @property
    def current_time(self):
        return self._clock

    def get_entity(self, lookup: str) -> Union[SimEntity, List[SimEntity]]:
        pattern = r"\b[A-Z][a-zA-Z0-9]*#\d+\b"
        if re.match(pattern, lookup):
            return self._entities_uid_map.get(lookup, None)
        else:
            result = self._entities.get(lookup, None)
            if result is None:
                raise ValueError(f"Could not find an entity with lookup term {lookup}")
            return result if len(result) > 1 else result[0]

    def add_event(self, event: SimEvent):
        self._queue.put(event)

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
        for _, entity in self._entities_uid_map.items():
            entity.start_entity()

    def run(self) -> None:
        if self.current_time == self.limit or len(self._queue) == 0:
            return self.terminate_simulation()
        self.clock()
        events = self._queue.get_next(self.current_time)
        for event in events:
            destination = self.get_entity(event.destination)
            destination.process_event(event)
        self.run()

    def terminate_simulation(self):
        for _, entities in self._entities.items():
            for entity in entities:
                entity.stop_entity()

    def register(self, entity: SimEntity):
        entity._platform = self
        self.add_entity(entity)

