from core.entities import SimEntity
from core.mixins import ContainerAccessMixin


class Invoker(SimEntity, ContainerAccessMixin):
    entity_type = 'invoker'