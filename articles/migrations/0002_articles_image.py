# Generated by Django 4.2.3 on 2023-07-26 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='image',
            field=models.ImageField(blank=True, default='defalt.jpg', upload_to=''),
        ),
    ]