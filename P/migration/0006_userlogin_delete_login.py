# Generated by Django 4.2.5 on 2024-04-25 01:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("P", "0005_remove_login_name_login_idval"),
    ]

    operations = [
        migrations.CreateModel(
            name="Userlogin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("userid", models.CharField(default="1", max_length=122)),
                ("password", models.CharField(default="12345", max_length=122)),
            ],
        ),
        migrations.DeleteModel(
            name="login",
        ),
    ]
