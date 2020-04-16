from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class MembershipQuerySet(models.QuerySet):
    def student(self):
        return self.exclude(title__held_by='coach').exclude(title__held_by='alumni')

    def coach(self):
        return self.filter(title__held_by='coach')

    def active(self):
        most_recent_member = self.latest('year', '-semester')
        year, semester = (most_recent_member.year, most_recent_member.semester)
        return self.filter(year=year, semester=semester, public=True)


class StudentManager(models.Manager):
    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db).student()

    def active(self):
        try:
            return self.get_queryset().active()
        except ObjectDoesNotExist:
            return None


class CoachManager(models.Manager):
    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db).coach()

    def active(self):
        try:
            return self.get_queryset().active()
        except ObjectDoesNotExist:
            return None
