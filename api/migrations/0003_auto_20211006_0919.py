# Generated by Django 3.2.7 on 2021-10-06 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20211004_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='in_production',
        ),
        migrations.AlterField(
            model_name='interface',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
