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
