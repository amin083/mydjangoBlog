# Generated by Django 4.2.3 on 2023-09-16 17:44

from django.db import migrations, models
from django.contrib.auth.models import User


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('keyword', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=models.CASCADE, to='user.user')),
                ('body', models.TextField()),
                ('image', models.ImageField(blank=True, default='defalt.jpg', upload_to='')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]