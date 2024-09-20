# Generated by Django 5.1.1 on 2024-09-20 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('individual', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=355)),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_category', to='individual.individual')),
            ],
            options={
                'verbose_name_plural': '2. Categories',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('priority', models.CharField(choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')], default='low', max_length=20)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Postponed', 'Postponed'), ('Cancelled', 'Cancelled'), ('On Hold', 'On Hold')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_individual', to='individual.individual')),
            ],
            options={
                'verbose_name_plural': '1. Tasks',
            },
        ),
    ]
