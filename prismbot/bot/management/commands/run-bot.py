import os

from django.core.management.base import BaseCommand

from prismbot.bot.client import run


class Command(BaseCommand):
    help = "Runs the Discord bot"

    def add_arguments(self, parser):
        parser.add_argument("--token", help="The token for your bot", type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[Bot] - Starting bot..."))

        bot_token = ("token" in options and options["token"]) or os.environ.get(
            "DISCORD_BOT_TOKEN"
        )

        if bot_token:
            run(bot_token)
        else:
            self.stdout.write(self.style.ERROR("[Bot] - No token found!"))

        self.stdout.write(self.style.SUCCESS("[Bot] - Bot has been shut down."))
