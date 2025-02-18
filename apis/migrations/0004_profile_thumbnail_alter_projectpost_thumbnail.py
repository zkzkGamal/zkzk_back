# Generated by Django 4.2.5 on 2023-09-26 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_alter_projectpost_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='thumbnail',
            field=models.ImageField(blank=True, default='images/user.png', null=True, upload_to='images/user'),
        ),
        migrations.AlterField(
            model_name='projectpost',
            name='thumbnail',
            field=models.ImageField(blank=True, default='images/placeholder.png', null=True, upload_to='images/Project_post'),
        ),
    ]
