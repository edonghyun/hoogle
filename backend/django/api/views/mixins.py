from ..authentication import CsrfExemptSessionAuthentication


class BasePublicAPIMixin:
    authentication_classes = [
        CsrfExemptSessionAuthentication,
    ]

    def initial(self, request, *args, **kwargs):
        if request.query_params.get('paginate') == 'false':
            self.pagination_class = None
        return super().initial(request, *args, **kwargs)
