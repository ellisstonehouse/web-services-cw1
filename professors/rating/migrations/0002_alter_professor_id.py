# Generated by Django 5.0.6 on 2025-02-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rating", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="professor",
            name="ID",
            field=models.CharField(max_length=3, primary_key=True, serialize=False),
        ),
    ]
