from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import InputRequired
from wtforms import ValidationError
from app.models import Software, Idc, Server


class AddSoftwareForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    description = StringField('Description')

    def validate_name(self, field):
        software = Software.query.filter_by(name=field.data).first()
        if software is not None:
            raise ValidationError('%s already in use.' % field.data)


class EditSoftwareForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_name = StringField('Name', validators=[InputRequired()])
    e_description = StringField('description')

    def validate_name(self, field):
        print(field)
        software = Software.query.filter_by(name=field.data).first()
        if software is not None:
            raise ValidationError('%s already in use.' % field.data)


class AddIdcForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    zone = StringField('Zone')
    region = StringField('Region')
    description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(AddIdcForm, self).__init__(*args, **kwargs)
        self.zone.choices = [(i, i) for i in current_app.config['ZONE']]
        self.region.choices = [(i, i) for i in current_app.config['REGION']]

    @staticmethod
    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('%s already in use.' % field.data)


class EditIdcForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_name = StringField('Name', validators=[InputRequired()])
    e_zone = StringField('Zone')
    e_region = StringField('Region')
    e_description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(EditIdcForm, self).__init__(*args, **kwargs)
        self.zone.choices = [(i, i) for i in current_app.config['ZONE']]
        self.region.choices = [(i, i) for i in current_app.config['REGION']]

    @staticmethod
    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('%s already in use.' % field.data)


class AddServerForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    idc = SelectField('IDC', coerce=int)
    instance_id = StringField('instance_id')
    instance_type = StringField('instance_type')
    platform = StringField('platform')
    image_name = StringField('image_name')
    key_name = StringField('key_name')
    private_ip = StringField('Private_ip')
    public_ip = StringField('Public_ip')
    block_device = StringField('block_device')
    subnet = StringField('subnet')
    create_time = DateTimeField('create_time', format="%Y-%m-%d %H:%M:%S")
    category = StringField('Category')
    category_branch = StringField('Category_Branch')
    status = SelectField('Status', coerce=str)
    description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(AddServerForm, self).__init__(*args, **kwargs)
        self.idc.choices = [(0, 'Choose...')] + [(idc.id, idc.name) for idc in Idc.query.order_by(Idc.name).all()]
        self.status.choices = [(i, i) for i in current_app.config['SERVER_STATUS']]

    @staticmethod
    def validate_name(self, field):
        if Server.query.filter_by(name=field.data).first():
            raise ValidationError('%s already in use.' % field.data)


class EditServerForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_name = StringField('Name', validators=[InputRequired()])
    e_idc = SelectField('IDC', coerce=int)
    e_instance_id = StringField('instance_id')
    e_instance_type = StringField('instance_type')
    e_platform = StringField('platform')
    e_image_name = StringField('platform')
    e_key_name = StringField('key_name')
    e_private_ip = StringField('Private_ip')
    e_public_ip = StringField('Public_ip')
    e_block_device = StringField('block_device')
    e_subnet = StringField('subnet')
    e_create_time = DateTimeField('create_time', format="%Y-%m-%d %H:%M:%S")
    e_category = StringField('Category')
    e_category_branch = StringField('Category_Branch')
    e_status = SelectField('Status', coerce=str)
    e_description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(EditServerForm, self).__init__(*args, **kwargs)
        self.e_idc.choices = [(idc.id, idc.name) for idc in Idc.query.order_by(Idc.name).all()]
        self.e_status.choices = [(i, i) for i in current_app.config['SERVER_STATUS']]

    @staticmethod
    def validate_name(self, field):
        if Server.query.filter_by(name=field.data).first():
            raise ValidationError('%s already in use.' % field.data)
