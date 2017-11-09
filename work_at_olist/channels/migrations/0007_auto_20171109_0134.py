# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 01:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0006_auto_20171106_1807'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categorytree',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='categorytree',
            name='parent',
        ),
        migrations.AlterModelOptions(
            name='channel',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='channel',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='channels.Channel'),
        ),
        migrations.AddField(
            model_name='channel',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.RemoveField(
            model_name='channel',
            name='categories',
        ),
        migrations.AlterUniqueTogether(
            name='channel',
            unique_together=set([('name', 'tree_id')]),
        ),
        migrations.DeleteModel(
            name='CategoryTree',
        ),
    ]
