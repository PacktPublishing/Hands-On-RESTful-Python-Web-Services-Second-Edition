import pytest
from base64 import b64encode
from flask import current_app, json, url_for
from http_status import HttpStatus
from models import orm, NotificationCategory, Notification, User


TEST_USER_NAME = 'testuser'
TEST_USER_PASSWORD = 'T3s!p4s5w0RDd12#'


def get_accept_content_type_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def get_authentication_headers(username, password):
    authentication_headers = get_accept_content_type_headers()
    authentication_headers['Authorization'] = \
        'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    return authentication_headers


def test_request_without_authentication(client):
    """
    Ensure we cannot access a resource that requirest authentication without an appropriate authentication header
    """
    response = client.get(
        url_for('service.notificationlistresource', _external=True),
        headers=get_accept_content_type_headers())
    assert response.status_code == HttpStatus.unauthorized_401.value


def create_user(client, name, password):
    url = url_for('service.userlistresource', 
        _external=True)
    data = {'name': name, 'password': password}
    response = client.post(
        url, 
        headers=get_accept_content_type_headers(),
        data=json.dumps(data))
    return response


def create_notification_category(client, name):
    url = url_for('service.notificationcategorylistresource', 
        _external=True)
    data = {'name': name}
    response = client.post(
        url, 
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD),
        data=json.dumps(data))
    return response


def test_create_and_retrieve_notification_category(client):
    """
    Ensure we can create a new Notification Category and then retrieve it
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    new_notification_category_name = 'New Information'
    post_response = create_notification_category(client, new_notification_category_name)
    assert post_response.status_code == HttpStatus.created_201.value
    assert NotificationCategory.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['name'] == new_notification_category_name
    new_notification_category_url = post_response_data['url']
    get_response = client.get(
        new_notification_category_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['name'] == new_notification_category_name


def test_create_duplicated_notification_category(client):
    """
    Ensure we cannot create a duplicated Notification Category
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    new_notification_category_name = 'New Information'
    post_response = create_notification_category(client, new_notification_category_name)
    assert post_response.status_code == HttpStatus.created_201.value
    assert NotificationCategory.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['name'] == new_notification_category_name
    second_post_response = create_notification_category(client, new_notification_category_name)
    assert second_post_response.status_code == HttpStatus.bad_request_400.value
    assert NotificationCategory.query.count() == 1


def test_retrieve_notification_categories_list(client):
    """
    Ensure we can retrieve the notification categories list
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    new_notification_category_name_1 = 'Error'
    post_response_1 = create_notification_category(client, new_notification_category_name_1)
    assert post_response_1.status_code, HttpStatus.created_201.value
    new_notification_category_name_2 = 'Warning'
    post_response_2 = create_notification_category(client, new_notification_category_name_2)
    assert post_response_2.status_code, HttpStatus.created_201.value
    url = url_for('service.notificationcategorylistresource', _external=True)
    get_response = client.get(
        url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert len(get_response_data) == 2
    assert get_response_data[0]['name'] == new_notification_category_name_1
    assert get_response_data[1]['name'] == new_notification_category_name_2


def test_update_notification_category(client):
    """
    Ensure we can update the name for an existing notification category
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    new_notification_category_name_1 = 'Error 1'
    post_response_1 = create_notification_category(client, new_notification_category_name_1)
    assert post_response_1.status_code == HttpStatus.created_201.value
    post_response_data_1 = json.loads(post_response_1.get_data(as_text=True))
    new_notification_category_url = post_response_data_1['url']
    new_notification_category_name_2 = 'Error 2'
    data = {'name': new_notification_category_name_2}
    patch_response = client.patch(
        new_notification_category_url, 
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD),
        data=json.dumps(data))
    assert patch_response.status_code == HttpStatus.ok_200.value
    get_response = client.get(
        new_notification_category_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['name'] == new_notification_category_name_2


def create_notification(client, message, ttl, notification_category):
    url = url_for('service.notificationlistresource', 
        _external=True)
    data = {'message': message, 'ttl': ttl, 'notification_category': notification_category}
    response = client.post(
        url, 
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD),
        data=json.dumps(data))
    return response


def test_create_and_retrieve_notification(client):
    """
    Ensure we can create a new notification and then retrieve it
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    new_notification_message = 'Welcome to the eSports Competition'
    new_notification_category = 'Information'
    post_response = create_notification(client, new_notification_message, 15, new_notification_category)
    assert post_response.status_code == HttpStatus.created_201.value
    assert Notification.query.count() == 1
    # The notification should have created a new notification catagory
    assert NotificationCategory.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['message'] == new_notification_message
    new_notification_url = post_response_data['url']
    get_response = client.get(
        new_notification_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['message'] == new_notification_message
    assert get_response_data['notification_category']['name'] == new_notification_category


def test_create_duplicated_notification(client):
    """
    Ensure we cannot create a duplicated Notification
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    new_notification_message = 'Welcome to the 4th eSports Competition'
    new_notification_category = 'Information'
    post_response = create_notification(client, new_notification_message, 25, new_notification_category)
    assert post_response.status_code == HttpStatus.created_201.value
    assert Notification.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['message'] == new_notification_message
    new_notification_url = post_response_data['url']
    get_response = client.get(
        new_notification_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['message'] == new_notification_message
    assert get_response_data['notification_category']['name'] == new_notification_category
    second_post_response = create_notification(client, new_notification_message, 15, new_notification_category)
    assert second_post_response.status_code == HttpStatus.bad_request_400.value
    assert Notification.query.count() == 1


def test_retrieve_notifications_list(client):
    """
    Ensure we can retrieve the notifications paginated list
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    new_notification_message_1 = 'The winners will be announced in 1 minute'
    new_notification_category_1 = 'Information'
    post_response = create_notification(client, new_notification_message_1, 15, new_notification_category_1)
    assert post_response.status_code == HttpStatus.created_201.value
    assert Notification.query.count() == 1
    new_notification_message_2 = 'There is a problem with one score'
    new_notification_category_2 = 'Error'
    post_response = create_notification(client, new_notification_message_2, 10, new_notification_category_2)
    assert post_response.status_code == HttpStatus.created_201.value
    assert Notification.query.count() == 2
    get_first_page_url = url_for('service.notificationlistresource', _external=True)
    get_first_page_response = client.get(
        get_first_page_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_first_page_response.status_code == HttpStatus.ok_200.value
    get_first_page_response_data = json.loads(get_first_page_response.get_data(as_text=True))
    assert get_first_page_response_data['count'] == 2
    assert get_first_page_response_data['previous'] is None
    assert get_first_page_response_data['next'] is None
    assert get_first_page_response_data['results'] is not None
    assert len(get_first_page_response_data['results']) == 2
    assert get_first_page_response_data['results'][0]['message'] == new_notification_message_1
    assert get_first_page_response_data['results'][1]['message'] == new_notification_message_2
    get_second_page_url = url_for('service.notificationlistresource', page=2)
    get_second_page_response = client.get(
        get_second_page_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_second_page_response.status_code == HttpStatus.ok_200.value
    get_second_page_response_data = json.loads(get_second_page_response.get_data(as_text=True))
    assert get_second_page_response_data['previous'] is not None
    assert get_second_page_response_data['previous'] == url_for('service.notificationlistresource', page=1)
    assert get_second_page_response_data['next'] is None
    assert get_second_page_response_data['results'] is not None
    assert len(get_second_page_response_data['results']) == 0


#### New code for second part of Chapter 4
#### New code for second part of Chapter 4
#### New code for second part of Chapter 4
#### New code for second part of Chapter 4
#### New code for second part of Chapter 4
#### New code for second part of Chapter 4
#### New code for second part of Chapter 4
def test_update_notification(client):
    """
    Ensure we can update a single field for an existing notification
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    
    new_notification_message_1 = 'Fortnite has a new winner'
    new_notification_category_1 = 'Information'
    post_response = create_notification(client, new_notification_message_1, 30, new_notification_category_1)
    assert post_response.status_code == HttpStatus.created_201.value
    assert Notification.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    new_notification_url = post_response_data['url']
    new_displayed_times = 1
    new_displayed_once = True
    data = {'displayed_times': new_displayed_times, 'displayed_once': str.lower(str(new_displayed_once))}
    patch_response = client.patch(
        new_notification_url, 
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD),
        data=json.dumps(data))
    assert patch_response.status_code == HttpStatus.ok_200.value
    get_response = client.get(
        new_notification_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['displayed_times'] == new_displayed_times
    assert get_response_data['displayed_once'] == new_displayed_once


def test_create_and_retrieve_user(client):
    """
    Ensure we can create a new User and then retrieve it
    """
    new_user_name = TEST_USER_NAME
    new_user_password = TEST_USER_PASSWORD
    post_response = create_user(client, new_user_name, new_user_password)
    assert post_response.status_code == HttpStatus.created_201.value
    assert User.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['name'] == new_user_name
    new_user_url = post_response_data['url']
    get_response = client.get(
        new_user_url,
        headers=get_authentication_headers(new_user_name, new_user_password))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['name'] == new_user_name
