from peewee import IntegerField


class UnsignedIntegerField(IntegerField):
    field_type = "int unsigned"
