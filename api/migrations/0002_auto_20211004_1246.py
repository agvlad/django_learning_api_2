# Generated by Django 3.2.7 on 2021-10-04 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='network',
            old_name='ip_address',
            new_name='network_address',
        ),
        migrations.AddField(
            model_name='network',
            name='subnet_mask',
            field=models.PositiveIntegerField(default=24),
            preserve_default=False,
        ),
    ]
