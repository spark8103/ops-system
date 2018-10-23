from app import create_app, db
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_security.utils import hash_password
from app.models import User, Role, Department, Software

from flask import url_for, abort, request, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers as admin_helpers

app = create_app()
security = Security()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class MyModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


admin = Admin(
    app,
    'ops-system manager',
    base_template='admin/master.html',
    template_mode='bootstrap3',
)

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(Department, db.session))


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


@app.before_first_request
def create_user():
    db.create_all()
    if not Role.query.first():
        admin_user_role = Role(name='admin')
        db.session.add(admin_user_role)
        user_datastore.create_user(email='admin@admin.com', password=hash_password('admin123'), roles=[admin_user_role])
        db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'Department': Department, 'Software': Software}

