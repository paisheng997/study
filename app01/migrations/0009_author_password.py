# Generated by Django 2.2.1 on 2019-10-04 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='password',
            field=models.CharField(default=123, max_length=64),
        ),
    ]
