class BaseViewMixin:
    @property
    def user(self):
        return self.request.user
