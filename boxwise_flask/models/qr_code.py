"""Model for a qr_code in the database."""
from peewee import CharField, DateTimeField, IntegerField

from ..db import db


class QRCode(db.Model):
    code = CharField()
    created_on = DateTimeField()
    created_by = IntegerField()
    last_modified_on = IntegerField()

    def __str__(self):
        return self.code + " " + str(self.created_by)

    @staticmethod
    def get_a_code(id):
        qr_code = QRCode.select().where(QRCode.id == id).get()
        return qr_code
