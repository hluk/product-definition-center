# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0012_auto_20160928_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentBranch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('active', models.BooleanField(default=True)),
                ('global_component', models.ForeignKey(to='component.GlobalComponent', on_delete=models.CASCADE)),
                ('type', models.ForeignKey(to='component.ReleaseComponentType', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SLA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=300)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SLAToComponentBranch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eol', models.DateField()),
                ('branch', models.ForeignKey(related_name='slas', to='componentbranch.ComponentBranch', on_delete=models.CASCADE)),
                ('sla', models.ForeignKey(to='componentbranch.SLA', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='componentbranch',
            unique_together=set([('global_component', 'name', 'type')]),
        ),
        migrations.AlterUniqueTogether(
            name='slatocomponentbranch',
            unique_together=set([('sla', 'branch')]),
        )
    ]
