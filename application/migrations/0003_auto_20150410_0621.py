# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20150408_0626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search',
            name='class_size',
        ),
        migrations.AddField(
            model_name='material',
            name='upload_type',
            field=models.CharField(max_length=10, null=True, choices=[(b'original', b'original'), (b'updated', b'updated')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='class_size',
            field=models.IntegerField(default=30, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='doc',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/cs121/cs122-win-15-lingweic-xiaoruit/k12exchange/files'), null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='category',
            field=models.CharField(blank=True, max_length=15, null=True, choices=[(b'Presentation', b'Presentation'), (b'In-Class_Work', b'In-Class_Work'), (b'Homework', b'Homework'), (b'Game', b'Game'), (b'Test', b'Test')]),
            preserve_default=True,
        ),
    ]
