from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from http_status import HttpStatus
from models import orm, NotificationCategory, NotificationCategorySchema, Notification, NotificationSchema
from sqlalchemy.exc import SQLAlchemyError
from helpers import PaginationHelper
from flask_httpauth import HTTPBasicAuth
from flask import g
from models import User, UserSchema


auth = HTTPBasicAuth()


@auth.verify_password
def verify_user_password(name, password):
    user = User.query.filter_by(name=name).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


class AuthenticationRequiredResource(Resource):
    method_decorators = [auth.login_required]


user_schema = UserSchema()
service_blueprint = Blueprint('service', __name__)
notification_category_schema = NotificationCategorySchema()
notification_schema = NotificationSchema()
service = Api(service_blueprint)


class UserResource(AuthenticationRequiredResource):
    def get(self, id):
        user = User.query.get_or_404(id)
        result = user_schema.dump(user).data
        return result


class UserListResource(Resource):
    @auth.login_required
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=User.query,
            resource_for_url='service.userlistresource',
            key_name='results',
            schema=user_schema)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        user_dict = request.get_json()
        if not user_dict:
            response = {'user': 'No input data provided'}
            return response, HttpStatus.bad_request_400.value
        errors = user_schema.validate(user_dict)
        if errors:
            return errors, HttpStatus.bad_request_400.value
        user_name = user_dict['name']
        existing_user = User.query.filter_by(name=user_name).first()
        if existing_user is not None:
            response = {'user': 'An user with the name {} already exists'.format(user_name)}
            return response, HttpStatus.bad_request_400.value
        try:
            user = User(name=user_name)
            error_message, password_ok = \
                user.check_password_strength_and_hash_if_ok(user_dict['password'])
            if password_ok:
                user.add(user)
                query = User.query.get(user.id)
                dump_result = user_schema.dump(query).data
                return dump_result, HttpStatus.created_201.value
            else:
                return {"error": error_message}, HttpStatus.bad_request_400.value
        except SQLAlchemyError as e:
            orm.session.rollback()
            response = {"error": str(e)}
            return response, HttpStatus.bad_request_400.value


class NotificationResource(AuthenticationRequiredResource):
    def get(self, id):
        notification = Notification.query.get_or_404(id)
        dumped_notification = notification_schema.dump(notification).data
        return dumped_notification

    def patch(self, id):
        notification = Notification.query.get_or_404(id)
        notification_dict = request.get_json(force=True)
        print(notification_dict)
        if 'message' in notification_dict and notification_dict['message'] is not None:
            notification_message = notification_dict['message']
            if not Notification.is_message_unique(id=0, message=notification_message):
                response = {'error': 'A notification with the message {} already exists'.format(notification_message)}
                return response, HttpStatus.bad_request_400.value
            notification.message = notification_message
        if 'ttl' in notification_dict and notification_dict['ttl'] is not None:
            notification.duration = notification_dict['duration']
        if 'displayed_times' in notification_dict and notification_dict['displayed_times'] is not None:
            notification.displayed_times = notification_dict['displayed_times']
        if 'displayed_once' in notification_dict and notification_dict['displayed_once'] is not None:
            notification.displayed_once = notification_dict['displayed_once'] == 'true'
        dumped_notification, dump_errors = notification_schema.dump(notification)
        if dump_errors:
            return dump_errors, HttpStatus.bad_request_400.value
        validate_errors = notification_schema.validate(dumped_notification)
        if validate_errors:
            return validate_errors, HttpStatus.bad_request_400.value
        try:
            notification.update()
            return self.get(id)
        except SQLAlchemyError as e:
                orm.session.rollback()
                response = {"error": str(e)}
                return response, HttpStatus.bad_request_400.value
         
    def delete(self, id):
        notification = Notification.query.get_or_404(id)
        try:
            delete = notification.delete(notification)
            response = make_response()
            return response, HttpStatus.no_content_204.value
        except SQLAlchemyError as e:
                orm.session.rollback()
                response = {"error": str(e)}
                return response, HttpStatus.unauthorized_401.value


class NotificationListResource(AuthenticationRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=Notification.query,
            resource_for_url='service.notificationlistresource',
            key_name='results',
            schema=notification_schema)
        pagination_result = pagination_helper.paginate_query()
        return pagination_result

    def post(self):
        notification_category_dict = request.get_json()
        if not notification_category_dict:
            response = {'message': 'No input data provided'}
            return response, HttpStatus.bad_request_400.value
        errors = notification_schema.validate(notification_category_dict)
        if errors:
            return errors, HttpStatus.bad_request_400.value
        notification_message = notification_category_dict['message']
        if not Notification.is_message_unique(id=0, message=notification_message):
            response = {'error': 'A notification with the message {} already exists'.format(notification_message)}
            return response, HttpStatus.bad_request_400.value
        try:
            notification_category_name = notification_category_dict['notification_category']['name']
            notification_category = NotificationCategory.query.filter_by(name=notification_category_name).first()
            if notification_category is None:
                # Create a new NotificationCategory
                notification_category = NotificationCategory(name=notification_category_name)
                orm.session.add(notification_category)
            # Now that we are sure we have a notification category,
            # we can create a new Notification
            notification = Notification(
                message=notification_message,
                ttl=notification_category_dict['ttl'],
                notification_category=notification_category)
            notification.add(notification)
            query = Notification.query.get(notification.id)
            dump_result = notification_schema.dump(query).data
            return dump_result, HttpStatus.created_201.value
        except SQLAlchemyError as e:
            orm.session.rollback()
            response = {"error": str(e)}
            return response, HttpStatus.bad_request_400.value


class NotificationCategoryResource(AuthenticationRequiredResource):
    def get(self, id):
        notification_category = NotificationCategory.query.get_or_404(id)
        dump_result = notification_category_schema.dump(notification_category).data
        return dump_result

    def patch(self, id):
        notification_category = NotificationCategory.query.get_or_404(id)
        notification_category_dict = request.get_json()
        if not notification_category_dict:
            response = {'message': 'No input data provided'}
            return response, HttpStatus.bad_request_400.value
        errors = notification_category_schema.validate(notification_category_dict)
        if errors:
            return errors, HttpStatus.bad_request_400.value
        try:
            if 'name' in notification_category_dict and notification_category_dict['name'] is not None:
                notification_category_name = notification_category_dict['name']
                if NotificationCategory.is_name_unique(id=id, name=notification_category_name):
                    notification_category.name = notification_category_name
                else:
                    response = {'error': 'A category with the name {} already exists'.format(notification_category_name)}
                    return response, HttpStatus.bad_request_400.value
            notification_category.update()
            return self.get(id)
        except SQLAlchemyError as e:
                orm.session.rollback()
                response = {"error": str(e)}
                return response, HttpStatus.bad_request_400.value
         
    def delete(self, id):
        notification_category = NotificationCategory.query.get_or_404(id)
        try:
            notification_category.delete(notification_category)
            response = make_response()
            return response, HttpStatus.no_content_204.value
        except SQLAlchemyError as e:
                orm.session.rollback()
                response = {"error": str(e)}
                return response, HttpStatus.unauthorized_401.value


class NotificationCategoryListResource(AuthenticationRequiredResource):
    def get(self):
        notification_categories = NotificationCategory.query.all()
        dump_results = notification_category_schema.dump(notification_categories, many=True).data
        return dump_results

    def post(self):
        print("Processing")
        notification_category_dict = request.get_json()
        if not notification_category_dict:
            response = {'message': 'No input data provided'}
            return response, HttpStatus.bad_request_400.value
        errors = notification_category_schema.validate(notification_category_dict)
        if errors:
            return errors, HttpStatus.bad_request_400.value
        notification_category_name = notification_category_dict['name']
        if not NotificationCategory.is_name_unique(id=0, name=notification_category_name):
            response = {'error': 'A notification category with the name {} already exists'.format(notification_category_name)}
            return response, HttpStatus.bad_request_400.value
        try:
            notification_category = NotificationCategory(notification_category_name)
            notification_category.add(notification_category)
            query = NotificationCategory.query.get(notification_category.id)
            dump_result = notification_category_schema.dump(query).data
            return dump_result, HttpStatus.created_201.value
        except SQLAlchemyError as e:
            print("Error")
            print(e)
            orm.session.rollback()
            response = {"error": str(e)}
            return response, HttpStatus.bad_request_400.value


service.add_resource(NotificationCategoryListResource, 
    '/notification_categories/')
service.add_resource(NotificationCategoryResource, 
    '/notification_categories/<int:id>')
service.add_resource(NotificationListResource, 
    '/notifications/')
service.add_resource(NotificationResource, 
    '/notifications/<int:id>')
service.add_resource(UserListResource, 
    '/users/')
service.add_resource(UserResource, 
    '/users/<int:id>')

