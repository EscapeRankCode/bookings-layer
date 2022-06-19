from flask import Flask
import app.api.api
import json

if __name__ == '__main__':
    app.api.api.rest.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
