# Generated by Django 2.2 on 2021-06-19 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('is_granted', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('granted_at', models.DateTimeField(auto_now=True)),
                ('user_that_like_wish', models.ManyToManyField(related_name='users_liked', to='wish_app.User')),
                ('wished_by', models.ForeignKey(default='SOME STRING', on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to='wish_app.User')),
            ],
        ),
    ]