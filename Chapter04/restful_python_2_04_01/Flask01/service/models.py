from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as password_context
import re


orm = SQLAlchemy()
ma = Marshmallow()


class ResourceAddUpdateDelete():   
    def add(self, resource):
        orm.session.add(resource)
        return orm.session.commit()

    def update(self):
        return orm.session.commit()

    def delete(self, resource):
        orm.session.delete(resource)
        return orm.session.commit()


class User(orm.Model, ResourceAddUpdateDelete):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(50), unique=True, nullable=False)
    # I save the hash for the password (I don't persist the actual password)
    password_hash = orm.Column(orm.String(120), nullable=False)
    creation_date = orm.Column(orm.TIMESTAMP, server_default=orm.func.current_timestamp(), nullable=False)

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)

    def check_password_strength_and_hash_if_ok(self, password):
        if len(password) < 8:
            return 'The password is too short. Please, specify a password with at least 8 characters.', False
        if len(password) > 32:
            return 'The password is too long. Please, specify a password with no more than 32 characters.', False
        if re.search(r'[A-Z]', password) is None:
            return 'The password must include at least one uppercase letter.', False
        if re.search(r'[a-z]', password) is None:
            return 'The password must include at least one lowercase letter.', False
        if re.search(r'\d', password) is None:
            return 'The password must include at least one number.', False
        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
            return 'The password must include at least one symbol.', False
        self.password_hash = password_context.hash(password)
        return '', True

    def __init__(self, name):
        self.name = name


class Notification(orm.Model, ResourceAddUpdateDelete):
    id = orm.Column(orm.Integer, primary_key=True)
    message = orm.Column(orm.String(250), unique=True, nullable=False)
    ttl = orm.Column(orm.Integer, nullable=False)
    creation_date = orm.Column(orm.TIMESTAMP, server_default=orm.func.current_timestamp(), nullable=False)
    notification_category_id = orm.Column(orm.Integer, orm.ForeignKey('notification_category.id', ondelete='CASCADE'), nullable=False)
    notification_category = orm.relationship('NotificationCategory', backref=orm.backref('notifications', lazy='dynamic' , order_by='Notification.message'))
    displayed_times = orm.Column(orm.Integer, nullable=False, server_default='0')
    displayed_once = orm.Column(orm.Boolean, nullable=False, server_default='false')

    @classmethod
    def is_message_unique(cls, id, message):
        existing_notification = cls.query.filter_by(message=message).first()
        if existing_notification is None:
            return True
        else:
            if existing_notification.id == id:
                return True
            else:
                return False

    def __init__(self, message, ttl, notification_category):
        self.message = message
        self.ttl = ttl
        self.notification_category = notification_category


class NotificationCategory(orm.Model, ResourceAddUpdateDelete):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(150), unique=True, nullable=False)

    @classmethod
    def is_name_unique(cls, id, name):
        existing_notification_category = cls.query.filter_by(name=name).first()
        if existing_notification_category is None:
            return True
        else:
            if existing_notification_category.id == id:
                return True
            else:
                return False
    
    def __init__(self, name):
        self.name = name


class NotificationCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    # Minimum length = 3 characters
    name = fields.String(required=True, 
        validate=validate.Length(3))
    url = ma.URLFor('service.notificationcategoryresource', 
        id='<id>', 
        _external=True)
    notifications = fields.Nested('NotificationSchema', 
        many=True, 
        exclude=('notification_category',))


class NotificationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    # Minimum length = 5 characters
    message = fields.String(required=True, 
        validate=validate.Length(5))
    ttl = fields.Integer()
    creation_date = fields.DateTime()
    notification_category = fields.Nested(NotificationCategorySchema, 
        only=['id', 'url', 'name'], 
        required=True)
    displayed_times = fields.Integer()
    displayed_once = fields.Boolean()
    url = ma.URLFor('service.notificationresource', 
        id='<id>', 
        _external=True)

    @pre_load
    def process_notification_category(self, data):
        notification_category = data.get('notification_category')
        if notification_category:
            if isinstance(notification_category, dict):
                notification_category_name = notification_category.get('name')
            else:
                notification_category_name = notification_category
            notification_category_dict = dict(name=notification_category_name)
        else:
            notification_category_dict = {}
        data['notification_category'] = notification_category_dict
        return data


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, 
        validate=validate.Length(3))
    url = ma.URLFor('service.userresource', 
        id='<id>', 
        _external=True)
