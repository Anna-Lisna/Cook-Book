# Generated by Django 4.1 on 2022-08-12 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_auth_token_check_customuser_auth_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='auth_token',
            new_name='email_token',
        ),
    ]