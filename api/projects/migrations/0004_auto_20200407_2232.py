# Generated by Django 3.0.4 on 2020-04-07 19:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_auto_20200406_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('planned_story_points', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='project',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='projects_participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('story_points', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('assigned_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Sprint')),
            ],
        ),
        migrations.AddField(
            model_name='sprint',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]
