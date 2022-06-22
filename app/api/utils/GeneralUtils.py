import json
from app.api.exceptions.general_exception import GeneralException


# CONSTANTS
ROUTES_FILE_PATH = "./app/api/routes.json"
SCHEMES_FILE_PATH = "./app/api/schemes.json"


# METHODS
def get_schemes():
    try:
        with open(SCHEMES_FILE_PATH, 'r') as schemes_file:
            schemes = json.loads(schemes_file.read())
            return schemes
    except Exception as e:
        raise GeneralException("get_schemes - " + str(e))


def get_routes():
    try:
        with open(ROUTES_FILE_PATH, 'r') as routes_file:
            routes = json.loads(routes_file.read())
            return routes
    except Exception as e:
        raise GeneralException("get_routes - " + str(e))
