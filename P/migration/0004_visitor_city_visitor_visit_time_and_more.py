# Generated by Django 4.2.4 on 2024-03-18 19:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('P', '0003_visitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='city',
            field=models.CharField(default='unknow', max_length=50),
        ),
        migrations.AddField(
            model_name='visitor',
            name='visit_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='purpose',
            field=models.CharField(max_length=255),
        ),
    ]