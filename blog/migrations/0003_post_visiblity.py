# Generated by Django 3.0.7 on 2020-06-25 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200625_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[(1, 'Public'), (2, 'Private')], default=1, max_length=1),
        ),
    ]
