
class ApiGeneralMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApiGeneral(metaclass=ApiGeneralMeta):
    def get_booking_system(self, api_request) -> str:
        return "{TuriTop}"
