from app import app, db
from app.models import User
from app.tools import cls

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'cls':cls}
