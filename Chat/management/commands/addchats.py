from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from Chat.models import ChatRoom, Member_ChatRoom
from Member.models import Member


class Command(BaseCommand):
    help = 'Add as many chats as you want'

    def add_arguments(self, parser):
        parser.add_argument('chat_cnt', type=int)

    def handle(self, *args, **options):
        chat_cnt = options['chat_cnt']
        if chat_cnt > 0:
            member = Member.objects.get(pk=1)

            ChatRoom.objects.bulk_create(
                [ChatRoom(name="Sample Room #{}".format(i), creator=member,
                          created_time=timezone.now(), location=member.location) for i in range(chat_cnt)]
            )
            rooms = ChatRoom.objects.filter(name__contains="Sample")
            Member_ChatRoom.objects.bulk_create(
                [Member_ChatRoom(member=member, chat_room=rooms[i],
                                 member_timestamp=timezone.now()) for i in range(chat_cnt)]
            )

            self.stdout.write(self.style.SUCCESS('Successfully add {} chats'.format(chat_cnt)))
