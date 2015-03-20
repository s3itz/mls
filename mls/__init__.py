import os

from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ['MLS_CONFIG_PATH'])

from . import api
from . import views
from . import models
from .database import Base, engine
Base.metadata.create_all(engine)

# During development mode; we'll display the config (including the key!)
if app.config.get('DEVELOPMENT', False):
    for key, value in sorted(os.environ.items()):
        if key.startswith('MLS_'):
            print("{}={}".format(key, value))