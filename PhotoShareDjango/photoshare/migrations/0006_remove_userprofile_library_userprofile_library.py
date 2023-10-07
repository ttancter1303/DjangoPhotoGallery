# Generated by Django 4.2.5 on 2023-10-07 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoshare', '0005_remove_image_image_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='library',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='library',
            field=models.ManyToManyField(blank=True, related_name='user_profiles', to='photoshare.image'),
        ),
    ]
