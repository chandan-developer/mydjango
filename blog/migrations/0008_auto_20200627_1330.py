# Generated by Django 3.0.7 on 2020-06-27 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200626_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraping',
            name='extracted_data',
            field=models.TextField(blank=True),
        ),
    ]
