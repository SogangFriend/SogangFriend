from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from Chat.models import ChatRoom, Member_ChatRoom
from Member.models import Member


class Command(BaseCommand):
    help = 'Remove all chats containing STRING in name'

    def add_arguments(self, parser):
        parser.add_argument('contain', type=str)

    def handle(self, *args, **options):
        contain = options['contain']

        rooms = ChatRoom.objects.filter(name__contains=contain)
        rooms.delete()

        self.stdout.write(self.style.SUCCESS('Successfully removed chats containing {}'.format(contain)))
