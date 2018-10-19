import base64
from datetime import datetime, timedelta
import os
import jwt
from time import time
from app import db, login
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, ValidationError, pre_load


class Permission:
    USER = 0x01
    WRITE_ARTICLES = 0x04
    ADMINISTER = 0x80


# MODELS #####
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.USER, True),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    description = db.Column(db.String(128))

    parent = db.relationship("Department", remote_side=[id, name])
    users = db.relationship('User', backref='department')
    # projects = db.relationship('Project', backref='department')

    def __repr__(self):
        return '<Department %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    mobile = db.Column(db.String(11))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __str__(self):
        return "User(id='%s')" % self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Idc(db.Model):
    __tablename__ = 'idcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    description = db.Column(db.String(256))

    idc = db.relationship('Server',
                          backref=db.backref('idc', lazy='joined'), lazy='dynamic')
    environments = db.relationship('Environment', backref='idc')

    def __repr__(self):
        return '<Idc %r>' % self.name


class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)   # server name
    idc_id = db.Column(db.Integer, db.ForeignKey('idcs.id'), index=True)  # idc info
    rack = db.Column(db.String(64))  # rack info
    private_ip = db.Column(db.String(128))  # private_ip
    public_ip = db.Column(db.String(128))  # public_ip
    category = db.Column(db.String(128), index=True)  # bigdata website
    category_branch = db.Column(db.String(128), index=True)  # prd-nginx prd-app
    env = db.Column(db.String(64), index=True)  # prd stg dev qa
    type = db.Column(db.String(128))  # server vserver
    status = db.Column(db.String(128))  # 在线 备用 维修
    description = db.Column(db.String(256))   # 备注说明

    def __repr__(self):
        return '<Server %r>' % self.name


class Software(db.Model):
    __tablename__ = 'software'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    version = db.Column(db.String(64), unique=True, index=True)

    modules = db.relationship('Module',
                         backref=db.backref('software', lazy='joined'), lazy='dynamic')

    @staticmethod
    def insert_softwares():
        softwares = {
            'nginx': 'nginx_1.12.2',
            'python3': 'python_3.7.0',
            'zabbix-agentd': 'zabbix-agentd'
        }
        for s in softwares:
            software = Software.query.filter_by(name=s).first()
            if software is None:
                software = Software(name=s)
            software.version = softwares[s]
            db.session.add(software)
        db.session.commit()

    def __repr__(self):
        return '<Software %r>' % self.name


# SCHEMAS #####


class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class DepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    parent = fields.Nested('self', only=["id", "name"])
    description = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    mobile = fields.Str()
    department = fields.Nested(DepartmentSchema, only=["id", "name"])
    role = fields.Nested(RoleSchema, only=["id", "name"])
    allow_login = fields.Boolean()
    type = fields.Str()
    member_since = fields.DateTime('%Y-%m-%d %H:%M:%S')
    last_seen = fields.DateTime('%Y-%m-%d %H:%M:%S')


class IdcSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()


class ServerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    idc = fields.Nested(IdcSchema, only=["id", "name"])
    rack = fields.Str()
    private_ip = fields.Str()
    public_ip = fields.Str()
    category = fields.Str()
    category_branch = fields.Str()
    env = fields.Str()
    type = fields.Str()
    status = fields.Str()
    description = fields.Str()


class SoftwareSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    version = fields.Str()


class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    department = fields.Nested(DepartmentSchema, only=["id", "name"])
    pm = fields.Nested(UserSchema, only=["id", "username"])
    sla = fields.Str()
    check_point = fields.Str()
    description = fields.Str()


class ModuleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    project = fields.Nested(ProjectSchema, only=["id", "name"])
    svn = fields.Str()
    parent = fields.Nested('self', only=["id", "name"])
    dev = fields.Nested(UserSchema, only=["id", "username"])
    qa = fields.Nested(UserSchema, only=["id", "username"])
    ops = fields.Nested(UserSchema, only=["id", "username"])
    software = fields.Nested(SoftwareSchema, only=["id", "version"])
    description = fields.Str()


class EnvironmentSchema(Schema):
    id = fields.Int(dump_only=True)
    module = fields.Nested(ModuleSchema, only=["id", "name"])
    idc = fields.Nested(IdcSchema, only=["id", "name"])
    env = fields.Str()
    check_point1 = fields.Str()
    check_point2 = fields.Str()
    check_point3 = fields.Str()
    deploy_path = fields.Str()
    server_ip = fields.Str()
    online_since = fields.Str('%Y-%m-%d %H:%M:%S')
    domain = fields.Str()


class DeploySchema(Schema):
    id = fields.Int(dump_only=True)
    module = fields.Nested(ModuleSchema, only=["id", "name"])
    parameter = fields.Str()
    ops = fields.Nested(UserSchema, only=["id", "username"])
    create_time = fields.Str('%Y-%m-%d %H:%M:%S')
    result = fields.String()