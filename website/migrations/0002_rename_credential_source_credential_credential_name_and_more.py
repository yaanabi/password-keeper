# Generated by Django 5.0.6 on 2024-06-14 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='credential',
            old_name='credential_source',
            new_name='credential_name',
        ),
        migrations.AddField(
            model_name='credential',
            name='credential_url',
            field=models.URLField(null=True),
        ),
    ]