# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 15:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0017_auto_20160527_1146'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TicketUserDetail',
            new_name='UserDetail',
        ),
        migrations.AddField(
            model_name='ticket',
            name='members',
            field=models.ManyToManyField(through='ticket.UserDetail', to=settings.AUTH_USER_MODEL),
        ),
    ]
