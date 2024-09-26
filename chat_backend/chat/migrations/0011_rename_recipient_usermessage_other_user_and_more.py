# Generated by Django 4.2 on 2024-09-24 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_alter_chathistory_communities_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermessage',
            old_name='recipient',
            new_name='other_user',
        ),
        migrations.AddField(
            model_name='usermessage',
            name='other_user_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
