# Generated by Django 3.2 on 2021-05-02 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("collegesearch", "0002_remove_region_neighbors")]

    operations = [
        migrations.AlterField(
            model_name="college",
            name="tuition_in_state",
            field=models.PositiveIntegerField(null=True),
        )
    ]
