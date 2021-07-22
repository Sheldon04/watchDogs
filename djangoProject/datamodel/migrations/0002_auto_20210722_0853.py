# Generated by Django 3.2.5 on 2021-07-22 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mypicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('photo', models.ImageField(default='user1.jpg', upload_to='photos')),
            ],
        ),
        migrations.DeleteModel(
            name='BookInfo',
        ),
    ]
