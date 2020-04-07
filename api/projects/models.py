from django.db import models
from django.core.validators import MinValueValidator


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    admin = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='projects_administration')
    participants = models.ManyToManyField('auth.User', related_name='projects_participation', blank=True)


class Sprint(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    planned_story_points = models.IntegerField(validators=[MinValueValidator(0)])
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    # weight = 
    story_points = models.IntegerField(validators=[MinValueValidator(0)])
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    assigned_person = models.ForeignKey('auth.User', on_delete=models.CASCADE)



