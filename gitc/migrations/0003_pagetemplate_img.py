# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-29 00:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitc', '0002_auto_20170728_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagetemplate',
            name='img',
            field=models.ImageField(default=1, upload_to='page', verbose_name='分析图'),
            preserve_default=False,
        ),
    ]