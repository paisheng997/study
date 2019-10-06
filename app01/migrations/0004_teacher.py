# Generated by Django 2.2.1 on 2019-09-15 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_book_publish'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('age', models.IntegerField(default=30)),
                ('gender', models.CharField(max_length=32)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app01.Person')),
            ],
            options={
                'db_table': 'teacher',
            },
        ),
    ]
