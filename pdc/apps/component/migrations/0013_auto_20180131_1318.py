# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0012_auto_20160928_1838'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='releasecomponent',
            options={'ordering': ('id',)},
        ),
    ]
