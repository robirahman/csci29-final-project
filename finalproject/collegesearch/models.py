from django.db.models import *


class College(Model):
    def __str__(self):
        return str(self.name)

    name = CharField(max_length=50)
    id = PositiveSmallIntegerField(primary_key=True)
    population = PositiveIntegerField()
    description = TextField()
    state = ForeignKey("State", on_delete=PROTECT, related_name="located_here")
    sat_min = PositiveSmallIntegerField()
    sat_max = PositiveSmallIntegerField()
    tuition = PositiveIntegerField()
    tuition_in_state = PositiveIntegerField(null=True)
    rating = PositiveSmallIntegerField()
    public = BooleanField()


class State(Model):
    def __str__(self):
        return str(self.name)

    name = CharField(max_length=25)
    id = PositiveSmallIntegerField(primary_key=True)
    region = ForeignKey("Region", on_delete=SET_NULL, null=True)


class Region(Model):
    def __str__(self):
        return str(self.name)

    name = CharField(max_length=25)
    id = PositiveSmallIntegerField(primary_key=True)
