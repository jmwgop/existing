# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 01:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConstantIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(max_length=20)),
                ('file_date', models.DateTimeField()),
                ('instrument_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='GranteeIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vp_index_id', models.IntegerField()),
                ('grantee', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='GrantorIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grantor', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ImgIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vp_index_id', models.IntegerField()),
                ('img_path', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LegalIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vp_index_id', models.IntegerField()),
                ('legal', models.CharField(max_length=45)),
                ('plss_block', models.CharField(max_length=15)),
                ('plss_block_ext', models.CharField(max_length=8)),
                ('plss_section', models.CharField(max_length=15)),
                ('addition_name', models.CharField(max_length=40)),
                ('lot_number', models.CharField(max_length=6)),
                ('lot_number_upper', models.CharField(max_length=6)),
                ('block', models.CharField(max_length=6)),
                ('plat_cabinet', models.CharField(max_length=6)),
                ('plat_page', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='VpDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vp_index_id', models.IntegerField()),
                ('volume', models.CharField(max_length=5)),
                ('page', models.CharField(max_length=4)),
                ('rec_type', models.CharField(max_length=2)),
                ('year', models.IntegerField()),
                ('doc_num', models.IntegerField()),
            ],
        ),
    ]
