from django.db import models
from sortedm2m.fields import SortedManyToManyField


class Member(models.Model):
    """Representation of a rotation member."""
    name = models.CharField(
        unique=True,
        max_length=255,
        help_text='The member\'s name.'
    )

    email = models.EmailField(
        unique=True,
        help_text='The member\'s email address, to which messages can be sent.'
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['-modified']

    def __str__(self):
        return '{name} <{email}>'.format(name=self.name, email=self.email)


class Rotation(models.Model):
    """Representation of a rotation."""
    name = models.CharField(
        unique=True,
        max_length=255,
        help_text='The rotation\'s name.'
    )

    description = models.TextField(
        help_text='A description of the rotation\'s purpose.'
    )

    message = models.TextField(
        help_text='A reminder message sent to members of the rotation.'
    )

    members = SortedManyToManyField(Member, related_name='rotations')
    watchers = SortedManyToManyField(Member, related_name='watching')

    on_call = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        help_text='Member currently on call.'
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['-modified']

    def __str__(self):
        return self.name
