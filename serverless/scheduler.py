import random

import settings
from core.entities import SimEntity, SimEvent
from core.mixins import InvokerAccessMixin
from core.simulator import Simulator

from .tags import ServerlessSimulationTags
from .request import ServerlessRequest


class Scheduler(SimEntity, InvokerAccessMixin):
    entity_type = "scheduler"

    def process_event(self, event: SimEvent):
        match event.tag:
            case ServerlessSimulationTags.SCHEDULE_INVOCATION:
                self.process_scheduling(event)
            case _:
                super().process_event(event)

    def process_scheduling(self, event: SimEvent):
        invokers = self.get_invokers()
        request: ServerlessRequest = event.get_data()
        warm_invokers = self._get_warm_invokers(invokers, request.function_id)
        selected_invoker = random.choice(warm_invokers if warm_invokers else invokers)
        self.send(Simulator.clock, selected_invoker, ServerlessSimulationTags.EXECUTE_FUNCTION, selected_invoker.uid)

    def _get_warm_invokers(self, invokers, function_id: int) -> list:
        pass


