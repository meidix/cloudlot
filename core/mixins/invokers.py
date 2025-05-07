from .base import BaseSimEntityAccessMixin


class InvokerAccessMixin(BaseSimEntityAccessMixin):

    def get_invokers(self):
        self.check_entity_access()
        return self._platform.get_entity("invoker")
