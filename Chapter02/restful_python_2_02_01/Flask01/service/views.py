from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from http_status import HttpStatus
from models import orm, NotificationCategory, NotificationCategorySchema, Notification, NotificationSchema
from sqlalchemy.exc import SQLAlchemyError


service_blueprint = Blueprint('service', __name__)
notification_category_schema = NotificationCategorySchema()
notification_schema = NotificationSchema()
service = Api(service_blueprint)


class NotificationResource(Resource):
    def get(self, id):
        notification = Notification.query.get_or_404(id)
        dumped_notification = notification_schema.dump(notification).data
        return dumped_notification

    def patch(self, id):
        notification = Notification.query.get_or_404(id)
        notification_dict = request.get_json(force=True)
        if 'message' in notification_dict and notification_dict['message'] is not None:
            notification.message = notification_dict['message']
        if 'ttl' in notification_dict and notification_dict['ttl'] is not None:
            notification.duration = notification_dict['duration']
        if 'displayed_times' in notification_dict and notification_dict['displayed_times'] is not None:
            notification.displayed_times = notification_dict['displayed_times']
        if 'displayed_once' in notification_dict and notification_dict['displayed_once'] is not None:
            notification.displayed_once = notification_dict['displayed_once']
        dumped_notification, dump_errors = notification_schema.dump(message)
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


class NotificationListResource(Resource):
    def get(self):
        notifications = Notification.query.all()
        dump_result = notification_schema.dump(notifications, many=True).data
        return dump_result

    def post(self):
        notification_category_dict = request.get_json()
        if not notification_category_dict:
            response = {'message': 'No input data provided'}
            return response, HttpStatus.bad_request_400.value
        errors = notification_schema.validate(notification_category_dict)
        if errors:
            return errors, HttpStatus.bad_request_400.value
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
                message=notification_category_dict['message'],
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


class NotificationCategoryResource(Resource):
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
            if 'name' in notification_category_dict and notification_category_dic['name'] is not None:
                notification_category.name = notification_category_dict['name']
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


class NotificationCategoryListResource(Resource):
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
        try:
            notification_category = NotificationCategory(notification_category_dict['name'])
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
