# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('componentbranch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentbranch',
            name='critical_path',
            field=models.BooleanField(default=False),
        ),
    ]
