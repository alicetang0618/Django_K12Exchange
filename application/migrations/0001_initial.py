# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=15, choices=[(b'Presentation', b'Presentation'), (b'In-Class_Work', b'In-Class_Work'), (b'Homework', b'Homework'), (b'Game', b'Game'), (b'Test', b'Test')])),
                ('doc', models.FileField(null=True, upload_to=b'files', blank=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('description', models.TextField()),
                ('grade', models.CharField(max_length=20, choices=[(b'kindergarten', b'kindergarten'), (b'elementary_school', b'elementary_school'), (b'middle_school', b'middle_school'), (b'high_school', b'high_school')])),
                ('year', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('subject', models.CharField(max_length=20)),
                ('class_size', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('tags', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(null=True, blank=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('material', models.ForeignKey(blank=True, to='application.Material', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=50, null=True, blank=True)),
                ('category', models.CharField(blank=True, max_length=1, null=True, choices=[(b'Presentation', b'Presentation'), (b'In-Class_Work', b'In-Class_Work'), (b'Homework', b'Homework'), (b'Game', b'Game'), (b'Test', b'Test')])),
                ('class_size', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('user_type', models.CharField(max_length=10, choices=[(b'Teacher', b'Teacher'), (b'Student', b'Student'), (b'Parent', b'Parent')])),
                ('school', models.CharField(max_length=50)),
                ('grade', models.CharField(max_length=20, choices=[(b'kindergarten', b'kindergarten'), (b'elementary_school', b'elementary_school'), (b'middle_school', b'middle_school'), (b'high_school', b'high_school')])),
                ('school_type', models.CharField(max_length=10, choices=[(b'private', b'private'), (b'public', b'public'), (b'charter', b'charter')])),
                ('geography', models.CharField(max_length=10, choices=[(b'urban', b'urban'), (b'suburb', b'suburb'), (b'rural', b'rural')])),
                ('city', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=15)),
                ('picture', models.ImageField(null=True, upload_to=b'profile_images', blank=True)),
                ('introduction', models.TextField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='search',
            name='user',
            field=models.ForeignKey(blank=True, to='application.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rating',
            name='rated',
            field=models.ForeignKey(related_name='rated', blank=True, to='application.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rating',
            name='rater',
            field=models.ForeignKey(related_name='rater', blank=True, to='application.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_by', null=True, to='application.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='uploader',
            field=models.ForeignKey(blank=True, to='application.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='material',
            field=models.ForeignKey(blank=True, to='application.Material', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='user',
            field=models.ForeignKey(blank=True, to='application.UserProfile', null=True),
            preserve_default=True,
        ),
    ]
