from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from tornado import web, escape, ioloop, httpclient, gen
from tornado.concurrent import run_on_executor
from drone import Altimeter, Hexacopter, LightEmittingDiode, Drone


thread_pool_executor = ThreadPoolExecutor()
drone = Drone()


class AsyncHexacopterHandler(web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "PATCH")
    HEXACOPTER_ID = 1
    _thread_pool_executor = thread_pool_executor

    @gen.coroutine
    def get(self, id):
        if int(id) is not self.__class__.HEXACOPTER_ID:
            self.set_status(HTTPStatus.NOT_FOUND)
            self.finish()
            return
        print("I've started retrieving the hexacopter's status")
        hexacopter_status = yield self.retrieve_hexacopter_status()
        print("I've finished retrieving the hexacopter's status")
        response = { 
            'motor_speed_in_rpm': hexacopter_status.motor_speed,
            'is_turned_on': hexacopter_status.is_turned_on,}
        self.set_status(HTTPStatus.OK)
        self.write(response)
        self.finish()

    @run_on_executor(executor="_thread_pool_executor")
    def retrieve_hexacopter_status(self):
        return drone.hexacopter.status
    
    @gen.coroutine
    def patch(self, id):
        if int(id) is not self.__class__.HEXACOPTER_ID:
            self.set_status(HTTPStatus.NOT_FOUND)
            self.finish()
            return
        request_data = escape.json_decode(self.request.body) 
        if ('motor_speed_in_rpm' not in request_data.keys()) or \
            (request_data['motor_speed_in_rpm'] is None):
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.finish()
            return
        try:
            motor_speed = int(request_data['motor_speed_in_rpm'])
            print("I've started setting the hexacopter's motor speed")
            hexacopter_status = yield self.set_hexacopter_motor_speed(motor_speed)
            print("I've finished setting the hexacopter's motor speed")
            response = { 
                'motor_speed_in_rpm': hexacopter_status.motor_speed,
                'is_turned_on': hexacopter_status.is_turned_on,}
            self.set_status(HTTPStatus.OK)
            self.write(response)
            self.finish()
        except ValueError as e:
            print("I've failed setting the hexacopter's motor speed")
            self.set_status(HTTPStatus.BAD_REQUEST)
            response = {
                'error': e.args[0]}
            self.write(response)
            self.finish()

    @run_on_executor(executor="_thread_pool_executor")
    def set_hexacopter_motor_speed(self, motor_speed):
        drone.hexacopter.motor_speed = motor_speed
        hexacopter_status = drone.hexacopter.status
        return hexacopter_status


class AsyncLedHandler(web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "PATCH")
    _thread_pool_executor = thread_pool_executor

    @gen.coroutine
    def get(self, id):
        int_id = int(id)
        if int_id not in drone.leds.keys():
            self.set_status(HTTPStatus.NOT_FOUND)
            self.finish()
            return
        led = drone.leds[int_id]
        print("I've started retrieving {0}'s status".format(led.description))
        brightness_level = yield self.retrieve_led_brightness_level(led)
        print("I've finished retrieving {0}'s status".format(led.description))
        response = {
            'id': led.id,
            'description': led.description,
            'brightness_level': brightness_level}
        self.set_status(HTTPStatus.OK)
        self.write(response)
        self.finish()

    @run_on_executor(executor="_thread_pool_executor")
    def retrieve_led_brightness_level(self, led):
        return led.brightness_level

    @gen.coroutine
    def patch(self, id):
        int_id = int(id)
        if int_id not in drone.leds.keys():
            self.set_status(HTTPStatus.NOT_FOUND)
            self.finish()
            return
        led = drone.leds[int_id]
        request_data = escape.json_decode(self.request.body) 
        if ('brightness_level' not in request_data.keys()) or \
            (request_data['brightness_level'] is None):
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.finish()
            return
        try:
            brightness_level = int(request_data['brightness_level'])
            print("I've started setting the {0}'s brightness level".format(led.description))
            yield self.set_led_brightness_level(led, brightness_level)
            print("I've finished setting the {0}'s brightness level".format(led.description))
            response = {
                'id': led.id,
                'description': led.description,
                'brightness_level': brightness_level}
            self.set_status(HTTPStatus.OK)
            self.write(response)
            self.finish()
        except ValueError as e:
            print("I've failed setting the {0}'s brightness level".format(led.description))
            self.set_status(HTTPStatus.BAD_REQUEST)
            response = {
                'error': e.args[0]}
            self.write(response)
            self.finish()

    @run_on_executor(executor="_thread_pool_executor")
    def set_led_brightness_level(self, led, brightness_level):
        led.brightness_level = brightness_level


class AsyncAltimeterHandler(web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    ALTIMETER_ID = 1
    _thread_pool_executor = thread_pool_executor

    @gen.coroutine
    def get(self, id):
        if int(id) is not self.__class__.ALTIMETER_ID:
            self.set_status(HTTPStatus.NOT_FOUND)
            self.finish()
            return
        unit = self.get_arguments(name='unit')
        if 'meters' in unit:
            altitude_multiplier = 0.3048
            response_unit = 'meters'
        else:
            altitude_multiplier = 1
            response_unit = 'feet'
        print("I've started retrieving the altitude")
        altitude_in_feet = yield self.retrieve_altitude_in_feet()
        altitude = round(altitude_in_feet * altitude_multiplier, 4)
        print("I've finished retrieving the altitude")
        response = { 
            'altitude': altitude,
            'unit': response_unit}
        self.set_status(HTTPStatus.OK)
        self.write(response)
        self.finish()

    @run_on_executor(executor="_thread_pool_executor")
    def retrieve_altitude_in_feet(self):
        return drone.altimeter.altitude


class Application(web.Application):
    def __init__(self, **kwargs):
        handlers = [
            (r"/hexacopters/([0-9]+)", AsyncHexacopterHandler),
            (r"/leds/([0-9]+)", AsyncLedHandler),
            (r"/altimeters/([0-9]+)", AsyncAltimeterHandler),
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
