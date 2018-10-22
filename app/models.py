from app import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    department = db.relationship('Department', backref=db.backref('users'))

    def __str__(self):
        return self.email

    # Custom User Payload
    def get_security_payload(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'last_login_ip': self.last_login_ip,
            'current_login_ip': self.current_login_ip,
            'login_count': self.login_count,
            'confirmed_at': self.confirmed_at
        }


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    description = db.Column(db.String(128))

    parent = db.relationship("Department", remote_side=[id, name])
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Department %r>' % self.name

    def __str__(self):
        return self.name

