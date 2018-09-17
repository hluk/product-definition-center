# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osbsrecord',
            name='component',
            field=models.OneToOneField(related_name='osbs', to='component.ReleaseComponent', on_delete=models.CASCADE),
        ),
    ]
