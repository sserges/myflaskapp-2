from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from config import Config

sentry_sdk.init(
    dsn="https://7ca9ef306f024243b0c1f33195ee1025@sentry.io/1301000",
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, errors
