from app import create_app, db
from app.models import Department, User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Department': Department, 'User': User}
