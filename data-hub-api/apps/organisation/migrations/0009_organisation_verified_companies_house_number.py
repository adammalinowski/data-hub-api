# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-13 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0008_auto_20160513_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='verified_companies_house_number',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]