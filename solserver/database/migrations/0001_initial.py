# Generated by Django 5.0.3 on 2024-03-09 20:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power_income', models.FloatField(null=True)),
                ('power_inject', models.FloatField(null=True)),
                ('power_consumption', models.FloatField(null=True)),
                ('battery', models.FloatField(null=True)),
                ('last_status_update', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('serial_number', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('software_version', models.CharField(max_length=6)),
                ('country', models.CharField(max_length=2)),
                ('postcode', models.CharField(max_length=4)),
                ('manufacturing_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SolMate',
            fields=[
                ('statusdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='database.statusdata')),
                ('productdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='database.productdata')),
                ('solmate_version', models.CharField(default='v1', max_length=30)),
                ('pv_connectors', models.IntegerField(default=1)),
                ('local_time', models.DateTimeField(null=True)),
            ],
            bases=('database.productdata', 'database.statusdata'),
        ),
    ]
