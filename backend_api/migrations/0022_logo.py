# Generated by Django 4.2.1 on 2023-11-14 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0021_alter_newuser_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
