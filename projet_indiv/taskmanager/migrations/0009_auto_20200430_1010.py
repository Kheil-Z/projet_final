# Generated by Django 2.1.15 on 2020-04-30 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0008_auto_20200430_0859'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'ordering': ['-date']},
        ),
    ]