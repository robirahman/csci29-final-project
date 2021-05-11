from django.db.models import *


class College(Model):
    """This class corresponds to the table of colleges and universities in our
    database, and each instance corresponds to one college that has a row in
    the table. They are indexed using their rank in Niche's top college list,
    and store other attributes collected from the US Department of Education's
    College Scorecard API on descriptors which are instances of Django fields."""
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
    """The database uses a snowflake schema with college locations stored
    as foreign keys to State objects rather than as strings. This allows
    states to be grouped into regions, and users can specify a preference
    to attend college in a geographical region, in which case colleges
    in those states are elevated in the results.

    Examples:
    >>> harvard = College.objects.filter(name="Harvard University")
    >>> print(harvard.state)
    "MA"
    >>> print(harvard.state.region)
    "New England"
    """
    def __str__(self):
        return str(self.name)

    name = CharField(max_length=25)
    id = PositiveSmallIntegerField(primary_key=True)
    region = ForeignKey("Region", on_delete=SET_NULL, null=True)


class Region(Model):
    """A Region is a geographical area within the United States,
    which has States (and thus Colleges) associated with it.

    Examples:
    >>> duke = College.objects.filter(name="Duke University")
    >>> clemson = College.objects.filter(name="Clemson University")
    >>> duke.state == clemson.state  # "NC" vs "SC"
    False
    >>> clemson.state.region == duke.state.region  # both in "Southeast"
    True
    """
    def __str__(self):
        return str(self.name)

    name = CharField(max_length=25)
    id = PositiveSmallIntegerField(primary_key=True)
