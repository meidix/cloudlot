from ..simulator import Simulator


class BaseSimEntityAccessMixin:
    _platform: Simulator


    def check_entity_access(self):
        if not hasattr(self, '_platform'):
            raise AttributeError("Entity not registered")

