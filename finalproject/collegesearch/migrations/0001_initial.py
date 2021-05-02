# Generated by Django 3.2 on 2021-05-02 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Region",
            fields=[
                ("name", models.CharField(max_length=25)),
                (
                    "id",
                    models.PositiveSmallIntegerField(primary_key=True, serialize=False),
                ),
                (
                    "neighbors",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="collegesearch.region",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                ("name", models.CharField(max_length=25)),
                (
                    "id",
                    models.PositiveSmallIntegerField(primary_key=True, serialize=False),
                ),
                (
                    "region",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="collegesearch.region",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="College",
            fields=[
                ("name", models.CharField(max_length=50)),
                (
                    "id",
                    models.PositiveSmallIntegerField(primary_key=True, serialize=False),
                ),
                ("population", models.PositiveIntegerField()),
                ("description", models.TextField()),
                ("sat_min", models.PositiveSmallIntegerField()),
                ("sat_max", models.PositiveSmallIntegerField()),
                ("tuition", models.PositiveIntegerField()),
                ("tuition_in_state", models.PositiveIntegerField()),
                ("rating", models.PositiveSmallIntegerField()),
                ("public", models.BooleanField()),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="located_here",
                        to="collegesearch.state",
                    ),
                ),
            ],
        ),
    ]
