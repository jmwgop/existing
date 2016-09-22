# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-21 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import upload.validators


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_auto_20160920_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='runsheetrequest',
            name='author',
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='documents/%Y/%m/%d/%s', validators=[upload.validators.validate_file_extension]),
        ),
        migrations.DeleteModel(
            name='RunsheetRequest',
        ),
    ]
