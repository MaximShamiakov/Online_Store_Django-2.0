# Generated by Django 4.2.1 on 2023-07-15 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0002_rename_name_orders_name_orders_surname2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='surname',
            new_name='lastName',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='surname2',
            new_name='patronymic',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='telephone',
            new_name='phone',
        ),
    ]
