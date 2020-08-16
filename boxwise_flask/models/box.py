"""Model for a Box in the database."""
from ..db import db


class Box(db.Model):
    def __str__(self):
        return self.id
