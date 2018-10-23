from app import db
from flask import url_for
from flask_security import UserMixin, RoleMixin


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'data': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


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

    def __repr__(self):
        return '<Role %r>' % self.name

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

    def __repr__(self):
        return '<User %r>' % self.email

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


# cmdb db
class Idc(db.Model, PaginatedAPIMixin):
    __tablename__ = 'idc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    zone = db.Column(db.String(128))
    region = db.Column(db.String(128))
    description = db.Column(db.String(256))
    idc = db.relationship('Server',
                          backref=db.backref('idc', lazy='joined'), lazy='dynamic')

    def __repr__(self):
        return '<Idc %r>' % self.name

    def __str__(self):
        return self.name

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'zone': self.zone,
            'region': self.region,
            'description': self.description
        }
        return data


class Server(db.Model, PaginatedAPIMixin):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)   # server name
    idc_id = db.Column(db.Integer, db.ForeignKey('idc.id'))  # idc info
    instance_id = db.Column(db.String(128), index=True)   # instance id
    instance_type = db.Column(db.String(128))   # instance type
    platform = db.Column(db.String(64))   # platform ubuntu windows
    image_name = db.Column(db.String(128))   # image_name
    key_name = db.Column(db.String(128))   # key_name
    private_ip = db.Column(db.String(256))  # private_ip
    public_ip = db.Column(db.String(256))  # public_ip
    block_device = db.Column(db.String(256))  # block_device /dev/sda /dev/sdb
    subnet = db.Column(db.String(64))  # subnet
    create_time = db.Column(db.DateTime())  # create time
    category = db.Column(db.String(128), index=True)  # big_data website ops office
    category_branch = db.Column(db.String(128), index=True)  # prd-gw prd-app

    status = db.Column(db.String(128))  # 在线 备用 维修
    description = db.Column(db.String(256))   # 备注说明

    def __repr__(self):
        return '<Server %r>' % self.name

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'idc': self.idc_id,
            'instance_id': self.instance_id,
            'instance_type': self.instance_type,
            'platform': self.platform,
            'image_name': self.image_name,
            'key_name': self.key_name,
            'private_ip': self.private_ip,
            'public_ip': self.public_ip,
            'block_device': self.block_device,
            'subnet': self.subnet,
            'create_time': self.create_time,
            'category': self.category,
            'category_branch': self.category_branch,
            'status': self.status,
            'description': self.description
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'idc_id', 'instance_id', 'instance_type', 'platform', 'image_name', 'key_name',
                      'private_ip', 'public_ip', 'block_device', 'subnet', 'create_time', 'category', 'category_branch',
                      'status', 'description']:
            if field in data:
                setattr(self, field, data[field])


class Software(db.Model, PaginatedAPIMixin):
    __tablename__ = 'software'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(128))

    def __repr__(self):
        return '<Software %r>' % self.name

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])
