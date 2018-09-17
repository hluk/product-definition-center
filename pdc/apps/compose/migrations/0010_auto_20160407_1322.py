# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150512_0703'),
        ('compose', '0009_auto_20160321_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComposeRelPath',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=2000)),
                ('arch', models.ForeignKey(to='common.Arch', on_delete=models.CASCADE)),
                ('compose', models.ForeignKey(to='compose.Compose', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='PathType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='composerelpath',
            name='type',
            field=models.ForeignKey(to='compose.PathType', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='composerelpath',
            name='variant',
            field=models.ForeignKey(to='compose.Variant', on_delete=models.CASCADE),
        ),
    ]
