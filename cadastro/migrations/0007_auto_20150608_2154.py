# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0006_auto_20150608_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='servercliente',
            name='criacao',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servercliente',
            name='ativacao',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
