# Generated by Django 3.2.7 on 2022-02-21 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0007_receiptinstance_confirmation_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiptinstance',
            name='confirmation_url',
        ),
    ]
