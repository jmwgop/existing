# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-27 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_auto_20160926_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runrequestdocs',
            name='request_id',
            field=models.IntegerField(),
        ),
    ]
