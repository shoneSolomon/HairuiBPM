# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-01 02:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitc', '0007_auto_20170731_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='html',
            name='url',
        ),
        migrations.AddField(
            model_name='html',
            name='html',
            field=models.TextField(default='1', verbose_name='代码'),
            preserve_default=False,
        ),
    ]