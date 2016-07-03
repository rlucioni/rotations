import calendar
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
import sendgrid

from rotations.models import Rotation


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Advance rotations, sending email reminders to members."""
    help = 'Advance rotations, sending email reminders to members.'
    rotation_day_name = calendar.day_name[settings.ROTATION_DAY]
    sendgrid_client = None

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Force execution. By default, the command only runs on {}.'.format(self.rotation_day_name)
        )

    def handle(self, *args, **options):
        force = options.get('force')

        if not self.is_runnable(force):
            return

        self.sendgrid_client = sendgrid.SendGridClient(
            settings.SENDGRID_USERNAME,
            settings.SENDGRID_PASSWORD,
        )

        rotations = Rotation.objects.all()
        logger.info('Attempting to advance %d rotations.', len(rotations))

        for rotation in rotations:
            members = list(rotation.members.all())
            member_count = len(members)

            # Figure out where we are in the rotation, where to look for who's up next,
            # and where to look for who's after that. Remember that members are ordered!
            try:
                current_index = members.index(rotation.on_call)
            except ValueError:
                logger.warning(
                    'Failed to find %s in the %s rotation\'s members list.',
                    rotation.on_call.name,
                    rotation.name,
                )
                current_index = 0

            next_index = (current_index + 1) % member_count
            next_member = members[next_index]

            future_index = (current_index + 2) % member_count
            future_member = members[future_index]

            # Advance the rotation.
            logger.info(
                'Advancing the %s rotation. %s was on call. %s is now on call.',
                rotation.name,
                next_member.name,
                future_member.name,
            )
            rotation.on_call = next_member
            rotation.save()

            # Notify all members of the change.
            self.notify(rotation, future_member)

    def is_runnable(self, force):
        """Determine if the command should be run."""
        if force:
            return True
        else:
            weekday = datetime.datetime.now().weekday()
            if weekday == settings.ROTATION_DAY:
                return True
            else:
                logger.info(
                    'Today is %s. This command only runs on %s. Exiting.',
                    calendar.day_name[weekday],
                    self.rotation_day_name,
                )
                return False

    def notify(self, rotation, up_next):
        logger.info('Notifying members of changes to the %s rotation.', rotation.name)

        text = rotation.message.format(
            rotation_name=rotation.name,
            on_call=rotation.on_call.name,
            up_next=up_next.name,
        )

        messages = [
            sendgrid.Mail(
                to=m.email,
                from_email=settings.FROM_EMAIL,
                subject=rotation.name,
                text=text,
            ) for m in rotation.members.all()
        ]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.sendgrid_client.send, m) for m in messages]

        for future in as_completed(futures):
            status, msg = future.result()
            log_msg = 'SendGrid returned {status}: {msg}.'.format(status=status, msg=msg)
            logger.info(log_msg) if status == 200 else logger.error(log_msg)
