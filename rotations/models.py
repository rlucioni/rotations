import logging

from django.db import models
from sortedm2m.fields import SortedManyToManyField


logger = logging.getLogger(__name__)


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

    def advance(self):
        """Advance the rotation to the next member in line."""
        members = list(self.members.all())
        member_count = len(members)

        # Figure out where we are in the rotation, where to look for who's up next,
        # and where to look for who's after that. Remember that members are ordered!
        try:
            current_index = members.index(self.on_call)
        except ValueError:
            logger.warning(
                'Failed to find %s in the %s rotation\'s members list.',
                self.on_call.name,
                self.name,
            )
            current_index = 0

        on_call_index = (current_index + 1) % member_count
        on_call_member = members[on_call_index]

        next_index = (current_index + 2) % member_count
        next_member = members[next_index]

        # Advance the rotation.
        logger.info(
            'Advancing the %s rotation. %s was on call. %s is now on call. %s is up next.',
            self.name,
            self.on_call.name,
            on_call_member.name,
            next_member.name,
        )

        self.on_call = on_call_member
        self.save()

        return next_member
