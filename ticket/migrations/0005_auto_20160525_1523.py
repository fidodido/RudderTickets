# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_auto_20160525_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='comment',
            field=models.CharField(blank=True, default=b'', max_length=255),
        ),
    ]
