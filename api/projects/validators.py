from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_start_date(start_date, end_date, latest_end_date):
    if start_date > end_date:
        raise ValidationError(
            _('Start date must be earlier than end date.'),
        )

    if start_date < latest_end_date:
        raise ValidationError(
            _('Overlapping sprints are not allowed! Latest sprint in this project ends on  %(value)s.'),
            params={'value': latest_end_date},
        )


def validate_task_vs_project(project, sprints):
    sprints = sprints.all()
    for sprint in sprints:
        if sprint.project.id != project.id:
            raise ValidationError(
                _('The task "%(value)s" cannot be added to this sprint because it belong to a different project.'),
                params={'value': sprint.id},
            )
