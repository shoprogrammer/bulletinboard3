# Generated by Django 5.1.4 on 2024-12-08 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_reactionmodel_content_reactionmodel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
