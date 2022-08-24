from app.api.modules.auth.adapters.simplybook.simplybook_auth import SimplybookApiAuth
from app.api.utils import general_utils


class ApiAuthMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ApiAuth(metaclass=ApiAuthMeta):
    def __init__(self):
        self.simplybook_api_auth = SimplybookApiAuth()

    def authorize(self, auth_credentials, booking_system_id: int):
        if booking_system_id == general_utils.BS_ID_SIMPLYBOOK:
            return self.simplybook_api_auth.authorize(auth_credentials)
        return None
