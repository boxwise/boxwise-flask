from peewee import (
    SQL,
    CharField,
    DateTimeField,
    DeferredForeignKey,
    ForeignKeyField,
    IntegerField,
)

from boxwise_flask.db import db
from boxwise_flask.models.organisation import Organisation
from boxwise_flask.models.usergroup_access_level import UsergroupAccessLevel


class Usergroup(db.Model):
    allow_borrow_adddelete = IntegerField()
    allow_laundry_block = IntegerField(constraints=[SQL("DEFAULT 0")])
    allow_laundry_startcycle = IntegerField(constraints=[SQL("DEFAULT 0")])
    created = DateTimeField(null=True)
    created_by = DeferredForeignKey("User")
    deleted = DateTimeField(null=True)
    label = CharField(null=True)
    modified = DateTimeField(null=True)
    modified_by = DeferredForeignKey("User")
    organisation = ForeignKeyField(
        column_name="organisation_id", field="id", model=Organisation
    )
    userlevel = ForeignKeyField(
        column_name="userlevel", field="id", model=UsergroupAccessLevel
    )

    class Meta:
        table_name = "cms_usergroups"

    def __str__(self):
        return self.id
