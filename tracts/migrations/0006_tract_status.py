# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracts', '0005_auto_20161011_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='tract',
            name='status',
            field=models.CharField(choices=[('LSE', 'Leased'), ('PLSE', 'Partially Leased'), ('OWN', 'Purchased'), ('POWN', 'Partially Purchased'), ('CLSE', 'Competitor'), ('PCLSE', 'Partial Competitor'), ('OP', 'Open')], default='OP', max_length=5),
        ),
    ]
