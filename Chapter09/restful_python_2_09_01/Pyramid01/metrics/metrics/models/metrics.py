from enum import Enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField


class SurfboardMetricModel:
    def __init__(self, status, speed_in_mph, altitude_in_feet, water_temperature_in_f):
        # We will automatically generate the new id
        self.id = 0
        self.status = status
        self.speed_in_mph = speed_in_mph
        self.altitude_in_feet = altitude_in_feet
        self.water_temperature_in_f = water_temperature_in_f


class SurfboardMetricManager():
    last_id = 0
    def __init__(self):
        self.metrics = {}

    def insert_metric(self, metric):
        self.__class__.last_id += 1
        metric.id = self.__class__.last_id
        self.metrics[self.__class__.last_id] = metric

    def get_metric(self, id):
        return self.metrics[id]

    def delete_metric(self, id):
        del self.metrics[id]


class SurferStatus(Enum):
    IDLE = 0
    PADDLING = 1
    RIDING = 2
    RIDE_FINISHED = 3
    WIPED_OUT = 4


class SurfboardMetricSchema(Schema):
    id = fields.Integer(dump_only=True)
    status = EnumField(enum=SurferStatus, required=True)
    speed_in_mph = fields.Integer(required=True)
    altitude_in_feet = fields.Integer(required=True)
    water_temperature_in_f = fields.Integer(required=True)