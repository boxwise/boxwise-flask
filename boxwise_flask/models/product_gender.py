from peewee import SQL, CharField, DateTimeField, ForeignKeyField, IntegerField

from boxwise_flask.db import db
from boxwise_flask.models.user import User


class ProductGender(db.Model):
    adult = IntegerField(constraints=[SQL("DEFAULT 0")])
    baby = IntegerField(constraints=[SQL("DEFAULT 0")])
    child = IntegerField(constraints=[SQL("DEFAULT 0")])
    color = CharField()
    created = DateTimeField(null=True)
    created_by = ForeignKeyField(
        column_name="created_by", field="id", model=User, null=True
    )
    female = IntegerField(constraints=[SQL("DEFAULT 0")])
    label = CharField()
    male = IntegerField(constraints=[SQL("DEFAULT 0")])
    modified = DateTimeField(null=True)
    modified_by = ForeignKeyField(
        backref="cms_users_modified_by_set",
        column_name="modified_by",
        field="id",
        model=User,
        null=True,
    )
    seq = IntegerField(null=True)
    shortlabel = CharField(null=True)

    class Meta:
        table_name = "genders"
