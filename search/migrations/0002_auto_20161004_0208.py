# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 02:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ConstantIndex',
        ),
        migrations.DeleteModel(
            name='GranteeIndex',
        ),
        migrations.DeleteModel(
            name='GrantorIndex',
        ),
        migrations.DeleteModel(
            name='ImgIndex',
        ),
        migrations.DeleteModel(
            name='LegalIndex',
        ),
        migrations.DeleteModel(
            name='VpDoc',
        ),
    ]
