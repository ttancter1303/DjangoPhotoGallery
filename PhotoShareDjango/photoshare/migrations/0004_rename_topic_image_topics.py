# Generated by Django 4.2.5 on 2023-10-02 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoshare', '0003_remove_image_topics_image_topic_alter_image_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='topic',
            new_name='topics',
        ),
    ]
