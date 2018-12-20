from async_drone_service import Application
from http import HTTPStatus
import json
import pytest
from tornado import escape


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
