# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('receiver', models.ForeignKey(related_name='receiver', blank=True, to='application.UserProfile', null=True)),
                ('sender', models.ForeignKey(related_name='sender', blank=True, to='application.UserProfile', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='search',
            name='class_size',
            field=models.IntegerField(default=30, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
    ]
