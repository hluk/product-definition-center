# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0008_auto_20160719_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariantCPE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpe', models.CharField(max_length=300)),
                ('variant', models.OneToOneField(to='release.Variant', on_delete=models.CASCADE)),
            ],
        ),
    ]
