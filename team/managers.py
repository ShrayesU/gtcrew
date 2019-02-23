from django.db import models

class MembershipQuerySet(models.QuerySet):
    def student(self):
        return self.exclude(title__held_by='coach').exclude(title__held_by='alumni')

    def coach(self):
        return self.filter(title__held_by='coach')

    def active(self):
        most_recent_member = self.latest('year', '-semester')
        year, semester = (most_recent_member.year, most_recent_member.semester)
        return self.filter(year=year, semester=semester)

class StudentManager(models.Manager):
    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db).student()

    def active(self):
        return self.get_queryset().pdfs()

class CoachManager(models.Manager):
    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db).coach()

    def active(self):
        return self.get_queryset().pdfs()
