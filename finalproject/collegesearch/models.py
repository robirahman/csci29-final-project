from django.contrib.auth.models import AbstractUser
from django.db.models import *


class User(AbstractUser):
    def __str__(self):
        return str(self.username)


class College(Model):
    def __str__(self):
        return str(self.name)

    name = CharField()
    id = PositiveSmallIntegerField(primary_key=True)
    population = PositiveIntegerField()
    description = TextField()
    state = ForeignKey("State", on_delete=PROTECT, related_name="located_here")
    sat_min = PositiveSmallIntegerField()
    sat_max = PositiveSmallIntegerField()
    tuition = PositiveIntegerField()
    tuition_in_state = PositiveIntegerField()
    rating = PositiveSmallIntegerField()
    public = BooleanField()


class State(Model):
    name = CharField()
    id = PositiveSmallIntegerField(primary_key=True)
    region = ForeignKey("Region", on_delete=SET_NULL)


class Region(Model):
    name = CharField()
    id = PositiveSmallIntegerField(primary_key=True)
    neighbors = ForeignKey("Region", on_delete=SET_NULL)
