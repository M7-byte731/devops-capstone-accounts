import os
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

talisman = Talisman(app, force_https=False)
CORS(app)

from service import routes  # noqa: E402,F401
