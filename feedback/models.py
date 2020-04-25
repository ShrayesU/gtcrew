from cuser.middleware import CuserMiddleware
from django.db import models
from django.contrib.auth import get_user_model

from feedback.utils import FEEDBACK_STATUS_CHOICES, OPEN


class Feedback(models.Model):
    status = models.CharField(
        max_length=8,
        choices=FEEDBACK_STATUS_CHOICES,
        default=OPEN,
    )
    feedback = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='feedback_submitted',
    )

    def __str__(self):
        return '%s on %s' % (self.created_by, self.date_added)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if not self.pk:
            self.created_by = user
        super(Feedback, self).save(*args, **kwargs)
