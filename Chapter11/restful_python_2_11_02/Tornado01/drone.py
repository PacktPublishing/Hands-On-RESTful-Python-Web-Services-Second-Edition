from time import sleep
from random import randint


class HexacopterStatus:
    def __init__(self, motor_speed, is_turned_on):
        self.motor_speed = motor_speed
        self.is_turned_on = is_turned_on


class Hexacopter:
    MIN_MOTOR_SPEED = 0
    MAX_MOTOR_SPEED = 500

    def __init__(self):
        self._motor_speed = self.__class__.MIN_MOTOR_SPEED
        self._is_turned_on = False

    @property
    def motor_speed(self):
        return self._motor_speed

    @motor_speed.setter    
    def motor_speed(self, value):
        if value < self.__class__.MIN_MOTOR_SPEED:
            raise ValueError('The minimum speed is {0}'.format(self.__class__.MIN_MOTOR_SPEED))
        if value > self.__class__.MAX_MOTOR_SPEED:
            raise ValueError('The maximum speed is {0}'.format(self.__class__.MAX_MOTOR_SPEED))
        self._motor_speed = value
        self._is_turned_on = (self.motor_speed is not 0)
        sleep(2)

    @property
    def is_turned_on(self):
        return self._is_turned_on

    @property
    def status(self):
        sleep(3)
        return HexacopterStatus(self.motor_speed, self.is_turned_on)


class LightEmittingDiode:
    MIN_BRIGHTNESS_LEVEL = 0
    MAX_BRIGHTNESS_LEVEL = 255

    def __init__(self, id, description):
        self.id = id
        self.description = description
        self._brightness_level = self.__class__.MIN_BRIGHTNESS_LEVEL

    @property
    def brightness_level(self):
        sleep(1)
        return self._brightness_level

    @brightness_level.setter
    def brightness_level(self, value):
        if value < self.__class__.MIN_BRIGHTNESS_LEVEL:
            raise ValueError('The minimum brightness level is {0}'.format(self.__class__.MIN_BRIGHTNESS_LEVEL))
        if value > self.__class__.MAX_BRIGHTNESS_LEVEL:
            raise ValueError('The maximum brightness level is {0}'.format(self.__class__.MAX_BRIGHTNESS_LEVEL))
        sleep(2)
        self._brightness_level = value


class Altimeter:
    @property
    def altitude(self):
        sleep(1)
        return randint(0, 3000)


class Drone:
    def __init__(self):
        self.hexacopter = Hexacopter()
        self.altimeter = Altimeter()
        self.red_led = LightEmittingDiode(1, 'Red LED')
        self.green_led = LightEmittingDiode(2, 'Green LED')
        self.blue_led = LightEmittingDiode(3, 'Blue LED')
        self.leds = {
            self.red_led.id: self.red_led,
            self.green_led.id: self.green_led,
            self.blue_led.id: self.blue_led}


if __name__ == '__main__':
    hexacopter = Hexacopter()
    hexacopter.motor_speed = 100
    print(hexacopter.is_turned_on)
    print(hexacopter.motor_speed)
    print(hexacopter.status.motor_speed)
    print(hexacopter.status.is_turned_on)
