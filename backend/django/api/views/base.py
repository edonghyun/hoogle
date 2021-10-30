from rest_framework.generics import GenericAPIView

from .mixins import BasePublicAPIMixin


class BasePublicAPIView(BasePublicAPIMixin, GenericAPIView):
    pass
