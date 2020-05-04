from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum

from .validators import validate_start_date, validate_task_vs_project


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    admin = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='projects_administration')
    participants = models.ManyToManyField('auth.User', related_name='projects_participation', blank=True)

    def __str__(self):
        return str(self.name)


class Sprint(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    # planned_story_points = models.IntegerField(validators=[MinValueValidator(0)])
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tasks = models.ManyToManyField('Task', related_name='sprints', blank=True)

    @property
    def planned_story_points(self):
        story_points_sum = Sprint.objects.get(id=self.id).tasks.all().aggregate(Sum('story_points'))['story_points__sum']
        if story_points_sum is not None:
            return story_points_sum
        return 0


class Task(models.Model):
    STATUS = [
        (0, 'To Do'),
        (1, 'In progress'),
        (2, 'Done'),
    ]

    WEIGHT = [
        (0, 'Low'),
        (1, 'Medium'),
        (2, 'High'),
        (3, 'Critical'),
    ]

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    weight = models.PositiveSmallIntegerField(choices=WEIGHT, default=1)
    story_points = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    assigned_person = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


