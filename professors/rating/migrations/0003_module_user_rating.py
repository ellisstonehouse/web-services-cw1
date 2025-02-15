# Generated by Django 5.0.6 on 2025-02-11 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rating", "0002_alter_professor_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "ID",
                    models.CharField(max_length=3, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "username",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("email", models.CharField(max_length=200, null=True)),
                ("password", models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                ("ID", models.AutoField(primary_key=True, serialize=False)),
                ("year", models.IntegerField()),
                ("semester", models.IntegerField()),
                ("rating", models.IntegerField()),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rating.module"
                    ),
                ),
                ("professors", models.ManyToManyField(to="rating.professor")),
            ],
        ),
    ]
