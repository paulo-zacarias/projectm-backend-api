from django.db import models
from django.core.validators import MinValueValidator
from .validators import validate_start_date
from django.db.models import Sum


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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def clean(self, *args, **kwargs):
        latest_end_date = Sprint.objects.all().filter(project=self.project).latest('end_date').end_date
        validate_start_date(self.start_date, self.end_date, latest_end_date)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Sprint, self).save(*args, **kwargs)

    @property
    def planned_story_points(self):
        story_points_sum = Task.objects.filter(sprint=self.id).aggregate(Sum('story_points'))['story_points__sum']
        if story_points_sum is not None:
            return story_points_sum
        return 0


class Task(models.Model):
    STATUS = [
        (0, 'Backlog'),
        (1, 'To Do'),
        (2, 'In progress'),
        (3, 'Done'),
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
    story_points = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    assigned_person = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)



