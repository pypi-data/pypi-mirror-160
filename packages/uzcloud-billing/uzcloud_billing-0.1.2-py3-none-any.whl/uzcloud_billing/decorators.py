from django.utils import timezone


def auth_required(func):
    def wrapper(self, *args, **kwargs):
        if self.AUTH_TOKEN is None:
            self.authorize()
        else:
            now = timezone.now()
            exp = timezone.datetime.fromtimestamp(self.DECODED.get("exp", None))
            if now > exp:
                self.authorize()
        return func(self, *args, **kwargs)

    return wrapper
