# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 19:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('left', models.PositiveIntegerField(null=True)),
                ('rigth', models.PositiveIntegerField(null=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='channels.Category')),
            ],
        ),
    ]
