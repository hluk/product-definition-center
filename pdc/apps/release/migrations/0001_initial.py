# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#


from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_product_id', models.CharField(unique=True, max_length=200)),
                ('short', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex=b'^[a-z\\-]+$', message=b'Only accept lowercase letter or -')])),
                ('version', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('base_product_id',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('short', models.CharField(unique=True, max_length=200, validators=[django.core.validators.RegexValidator(regex=b'^[a-z\\-]+$', message=b'Only accept lowercase letter or -')])),
            ],
        ),
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('short', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex=b'^[a-z\\-]+$', message=b'Only accept lowercase letter or -')])),
                ('version', models.CharField(max_length=200)),
                ('product_version_id', models.CharField(max_length=200)),
                ('product', models.ForeignKey(to='release.Product', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release_id', models.CharField(unique=True, max_length=200)),
                ('short', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex=b'^[a-z\\-]+$', message=b'Only accept lowercase letter or -')])),
                ('version', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('base_product', models.ForeignKey(blank=True, to='release.BaseProduct', null=True, on_delete=models.CASCADE)),
                ('integrated_with', models.ForeignKey(related_name='integrated_releases', blank=True, to='release.Release', null=True, on_delete=models.CASCADE)),
                ('product_version', models.ForeignKey(blank=True, to='release.ProductVersion', null=True, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('release_id',),
            },
        ),
        migrations.CreateModel(
            name='ReleaseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('suffix', models.CharField(unique=True, max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('variant_id', models.CharField(max_length=100)),
                ('variant_uid', models.CharField(max_length=200)),
                ('variant_name', models.CharField(max_length=300)),
                ('deleted', models.BooleanField(default=False)),
                ('release', models.ForeignKey(to='release.Release', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('variant_uid',),
            },
        ),
        migrations.CreateModel(
            name='VariantArch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('arch', models.ForeignKey(to='common.Arch', on_delete=models.CASCADE)),
                ('variant', models.ForeignKey(to='release.Variant', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('variant', 'arch'),
            },
        ),
        migrations.CreateModel(
            name='VariantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='variant',
            name='variant_type',
            field=models.ForeignKey(to='release.VariantType', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='release',
            name='release_type',
            field=models.ForeignKey(to='release.ReleaseType', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='baseproduct',
            unique_together=set([('short', 'version'), ('name', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='variantarch',
            unique_together=set([('variant', 'arch')]),
        ),
        migrations.AlterUniqueTogether(
            name='variant',
            unique_together=set([('release', 'variant_uid')]),
        ),
        migrations.AlterUniqueTogether(
            name='release',
            unique_together=set([('short', 'version', 'release_type', 'base_product')]),
        ),
        migrations.AlterUniqueTogether(
            name='productversion',
            unique_together=set([('short', 'version')]),
        ),
    ]
