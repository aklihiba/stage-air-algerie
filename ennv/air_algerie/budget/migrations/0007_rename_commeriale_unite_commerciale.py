# Generated by Django 3.2.7 on 2021-10-12 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_alter_runion_etat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unite',
            old_name='commeriale',
            new_name='commerciale',
        ),
    ]
