from http import HTTPStatus
from datetime import date
from tornado import web, escape, ioloop, httpclient, gen
from drone import Altimeter, Hexacopter, LightEmittingDiode, Drone


drone = Drone()


class HexacopterHandler(web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "PATCH")
    HEXACOPTER_ID = 1

    def get(self, id):
        if int(id) is not self.__class__.HEXACOPTER_ID:
            self.set_status(HTTPStatus.NOT_FOUND)
            return
        print("I've started retrieving the hexacopter's status")
        hexacopter_status = drone.hexacopter.status
        print("I've finished retrieving the hexacopter's status")
        response = { 
            'motor_speed_in_rpm': hexacopter_status.motor_speed,
            'is_turned_on': hexacopter_status.is_turned_on,}
        self.set_status(HTTPStatus.OK)
        self.write(response)
    
    def patch(self, id):
        if int(id) is not self.__class__.HEXACOPTER_ID:
            self.set_status(HTTPStatus.NOT_FOUND)
            return
        request_data = escape.json_decode(self.request.body) 
        if ('motor_speed_in_rpm' not in request_data.keys()) or \
            (request_data['motor_speed_in_rpm'] is None):
            self.set_status(HTTPStatus.BAD_REQUEST)
            return
        try:
            motor_speed = int(request_data['motor_speed_in_rpm'])
            print("I've started setting the hexacopter's motor speed")
            drone.hexacopter.motor_speed = motor_speed
            hexacopter_status = drone.hexacopter.status
            print("I've finished setting the hexacopter's motor speed")
            response = { 
                'motor_speed_in_rpm': hexacopter_status.motor_speed,
                'is_turned_on': hexacopter_status.is_turned_on,}
            self.set_status(HTTPStatus.OK)
            self.write(response)
        except ValueError as e:
            print("I've failed setting the hexacopter's motor speed")
            self.set_status(HTTPStatus.BAD_REQUEST)
            response = {
                'error': e.args[0]}
            self.write(response)


class LedHandler(web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "PATCH")

    def get(self, id):
        int_id = int(id)
        if int_id not in drone.leds.keys():
            self.set_status(HTTPStatus.NOT_FOUND)
            return
        led = drone.leds[int_id]
        print("I've started retrieving {0}'s status".format(led.description))
        brightness_level = led.brightness_level
        print("I've finished retrieving {0}'s status".format(led.description))
        response = {
            'id': led.id,
            'description': led.description,
            'brightness_level': brightness_level}
        self.set_status(HTTPStatus.OK)
        self.write(response)

    def patch(self, id):
        int_id = int(id)
        if int_id not in drone.leds.keys():
            self.set_status(HTTPStatus.NOT_FOUND)
            return
        led = drone.leds[int_id]
        request_data = escape.json_decode(self.request.body) 
        if ('brightness_level' not in request_data.keys()) or \
            (request_data['brightness_level'] is None):
            self.set_status(HTTPStatus.BAD_REQUEST)
            return
        try:
            brightness_level = int(request_data['brightness_level'])
            print("I've started setting the {0}'s brightness level".format(led.description))
            led.brightness_level = brightness_level
            print("I've finished setting the {0}'s brightness level".format(led.description))
            response = {
                'id': led.id,
                'description': led.description,
                'brightness_level': brightness_level}
            self.set_status(HTTPStatus.OK)
            self.write(response)
        except ValueError as e:
            print("I've failed setting the {0}'s brightness level".format(led.description))
            self.set_status(HTTPStatus.BAD_REQUEST)
            response = {
                'error': e.args[0]}
            self.write(response)


class AltimeterHandler(web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    ALTIMETER_ID = 1

    def get(self, id):
        if int(id) is not self.__class__.ALTIMETER_ID:
            self.set_status(HTTPStatus.NOT_FOUND)
            return
        unit = self.get_arguments(name='unit')
        if 'meters' in unit:
            altitude_multiplier = 0.3048
            response_unit = 'meters'
        else:
            altitude_multiplier = 1
            response_unit = 'feet'
        print("I've started retrieving the altitude")
        altitude = round(drone.altimeter.altitude * altitude_multiplier, 4)
        print("I've finished retrieving the altitude")
        response = { 
            'altitude': altitude,
            'unit': response_unit}
        self.set_status(HTTPStatus.OK)
        self.write(response)


class Application(web.Application):
    def __init__(self, **kwargs):
        handlers = [
            (r"/hexacopters/([0-9]+)", HexacopterHandler),
            (r"/leds/([0-9]+)", LedHandler),
            (r"/altimeters/([0-9]+)", AltimeterHandler),
        ]
        super(Application, self).__init__(handlers, **kwargs)


if __name__ == "__main__":
    application = Application()
    port = 8888
    print("Listening at port {0}".format(port))
    application.listen(port)
    tornado_ioloop = ioloop.IOLoop.instance()
    periodic_callback = ioloop.PeriodicCallback(lambda: None, 500)
    periodic_callback.start()
    tornado_ioloop.start()
