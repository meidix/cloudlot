from .base import BaseSimEntityAccessMixin


class InvokerMixin(BaseSimEntityAccessMixin):

    def get_invokers(self):
            self.check_entity_access()
            return self._platform.get_invokers()
