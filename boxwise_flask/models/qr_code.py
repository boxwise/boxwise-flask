"""Model definitions for database."""
from peewee import CharField, DateTimeField, IntegerField

from ..db import db
from .custom_fields import UnsignedIntegerField


class QRCode(db.Model):
    id = UnsignedIntegerField()
    code = CharField()
    created_on = DateTimeField()
    created_by = IntegerField()
    last_modified_on = IntegerField()

    def __str__(self):
        return id

    @staticmethod
    def get_a_code(id):
        qr_code = QRCode.select().where(QRCode.id == id).get()
        return qr_code
