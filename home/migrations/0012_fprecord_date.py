# Generated by Django 4.2.1 on 2023-07-30 03:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_fp'),
    ]

    operations = [
        migrations.AddField(
            model_name='fprecord',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]