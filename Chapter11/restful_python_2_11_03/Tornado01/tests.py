from async_drone_service import Application
from http import HTTPStatus
import json
import pytest
from tornado import escape
from tornado.httpclient import HTTPClientError


@pytest.fixture
def app():
    application = Application(debug=False)
    return application


async def test_set_and_get_leds_brightness_levels(http_server_client):
    """
    Ensure we can set and get the brightness levels for the three LEDs
    """
    for led_id in range(1, 4):
        patch_args = {'brightness_level': led_id * 60}
        patch_response = await http_server_client.fetch(
            '/leds/{}'.format(led_id), 
            method='PATCH', 
            body=json.dumps(patch_args))
        assert patch_response.code == HTTPStatus.OK
        get_response = await http_server_client.fetch(
            '/leds/{}'.format(led_id),
            method='GET')
        assert get_response.code == HTTPStatus.OK
        get_response_data = escape.json_decode(get_response.body)
        assert 'brightness_level' in get_response_data.keys()
        assert get_response_data['brightness_level'] == \
            patch_args['brightness_level']


async def test_set_and_get_hexacopter_motor_speed(http_server_client):
    """
    Ensure we can set and get the hexacopter's motor speed
    """
    patch_args = {'motor_speed_in_rpm': 200}
    patch_response = await http_server_client.fetch(
        '/hexacopters/1', 
        method='PATCH', 
        body=json.dumps(patch_args))
    assert patch_response.code == HTTPStatus.OK
    get_response = await http_server_client.fetch(
        '/hexacopters/1',
        method='GET')
    assert get_response.code == HTTPStatus.OK
    get_response_data = escape.json_decode(get_response.body)
    assert 'motor_speed_in_rpm' in get_response_data.keys()
    assert 'is_turned_on' in get_response_data.keys()
    assert get_response_data['motor_speed_in_rpm'] == patch_args['motor_speed_in_rpm']
    assert get_response_data['is_turned_on']


async def test_get_altimeter_altitude_in_feet(http_server_client):
    """
    Ensure we can get the altimeter's altitude in feet
    """
    get_response = await http_server_client.fetch(
        '/altimeters/1',
        method='GET')
    assert get_response.code == HTTPStatus.OK
    get_response_data = escape.json_decode(get_response.body)
    assert 'altitude' in get_response_data.keys()
    assert 'unit' in get_response_data.keys()
    assert get_response_data['altitude'] >= 0
    assert get_response_data['altitude'] <= 3000
    assert get_response_data['unit'] == 'feet'


async def test_get_altimeter_altitude_in_meters(http_server_client):
    """
    Ensure we can get the altimeter's altitude in meters
    """
    get_response = await http_server_client.fetch(
        '/altimeters/1?unit=meters',
        method='GET')
    assert get_response.code == HTTPStatus.OK
    get_response_data = escape.json_decode(get_response.body)
    assert 'altitude' in get_response_data.keys()
    assert 'unit' in get_response_data.keys()
    assert get_response_data['altitude'] >= 0
    assert get_response_data['altitude'] <= 914.4
    assert get_response_data['unit'] == 'meters'


async def test_set_invalid_brightness_level(http_server_client):
    """
    Ensure we cannot set an invalid brightness level for a LED
    """
    patch_args_led_1 = {'brightness_level': 256}
    try:
        patch_response_led_1 = await http_server_client.fetch(
            '/leds/1', 
            method='PATCH', 
            body=json.dumps(patch_args_led_1))
    except HTTPClientError as err:
        assert err.code == HTTPStatus.BAD_REQUEST
    patch_args_led_2 = {'brightness_level': -256}
    try:
        patch_response_led_2 = await http_server_client.fetch(
            '/leds/2', 
            method='PATCH', 
            body=json.dumps(patch_args_led_2))
    except HTTPClientError as err:
        assert err.code == HTTPStatus.BAD_REQUEST
    patch_args_led_3 = {'brightness_level': 512}
    try:
        patch_response_led_3 = await http_server_client.fetch(
            '/leds/3', 
            method='PATCH', 
            body=json.dumps(patch_args_led_3))
    except HTTPClientError as err:
        assert err.code == HTTPStatus.BAD_REQUEST


async def test_set_brightness_level_invalid_led_id(http_server_client):
    """
    Ensure we cannot set the brightness level for an invalid LED id
    """
    patch_args_led_1 = {'brightness_level': 128}
    try:
        patch_response_led_1 = await http_server_client.fetch(
            '/leds/100', 
            method='PATCH', 
            body=json.dumps(patch_args_led_1))
    except HTTPClientError as err:
        assert err.code == HTTPStatus.NOT_FOUND


async def test_get_brightness_level_invalid_led_id(http_server_client):
    """
    Ensure we cannot get the brightness level for an invalid LED id
    """
    try:
        patch_response_led_1 = await http_server_client.fetch(
            '/leds/100', 
            method='GET')
    except HTTPClientError as err:
        assert err.code == HTTPStatus.NOT_FOUND


async def test_set_invalid_motor_speed(http_server_client):
    """
    Ensure we cannot set an invalid motor speed for the hexacopter
    """
    patch_args_hexacopter_1 = {'motor_speed': 89000}
    try:
        patch_response_hexacopter_1 = await http_server_client.fetch(
            '/hexacopters/1', 
            method='PATCH', 
            body=json.dumps(patch_args_hexacopter_1))
    except HTTPClientError as err:
        assert err.code == HTTPStatus.BAD_REQUEST
    patch_args_hexacopter_2 = {'motor_speed': -78600}
    try:
        patch_response_hexacopter_2 = await http_server_client.fetch(
            '/hexacopters/1', 
            method='PATCH', 
            body=json.dumps(patch_args_hexacopter_2))
    except HTTPClientError as err:
        assert err.code == HTTPStatus.BAD_REQUEST
    patch_args_hexacopter_3 = {'motor_speed': 8900}
    try:
        patch_response_hexacopter_3 = await http_server_client.fetch(
            '/hexacopters/1', 
            method='PATCH', 
            body=json.dumps(patch_args_hexacopter_3))
    except HTTPClientError as err:
        assert err.code == HTTPStatus.BAD_REQUEST


async def test_set_motor_speed_invalid_hexacopter_id(http_server_client):
    """
    Ensure we cannot set the motor speed for an invalid hexacopter id
    """
    patch_args_hexacopter_1 = {'motor_speed': 128}
    try:
        patch_response_hexacopter_1 = await http_server_client.fetch(
            '/hexacopters/100', 
            method='PATCH', 
            body=json.dumps(patch_args_hexacopter_1))
    except HTTPClientError as err:
        assert err.code == HTTPStatus.NOT_FOUND


async def test_get_motor_speed_invalid_hexacopter_id(http_server_client):
    """
    Ensure we cannot get the motor speed for an invalid hexacopter id
    """
    try:
        patch_response_hexacopter_1 = await http_server_client.fetch(
            '/hexacopters/5', 
            method='GET')
    except HTTPClientError as err:
        assert err.code == HTTPStatus.NOT_FOUND


async def test_get_altimeter_altitude_invalid_altimeter_id(http_server_client):
    """
    Ensure we cannot get the altimeter's altitude for an invalid altimeter id
    """
    try:
        get_response = await http_server_client.fetch(
            '/altimeters/5',
            method='GET')
    except HTTPClientError as err:
        assert err.code == HTTPStatus.NOT_FOUND        
