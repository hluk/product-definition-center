# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150512_0703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='label',
            options={'ordering': ('name',)},
        ),
    ]
