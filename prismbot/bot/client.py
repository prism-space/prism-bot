import logging

import discord
from discord.ext import commands
from django.conf import settings

DISCORD_GUILD = discord.Object(id=settings.DISCORD_GUILD_ID)
INSTALLED_EXTENSIONS = ["prismbot.bot.commands.roles"]

logger = logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)


class BotClient(commands.Bot):
    def __init__(
        self, *, intents: discord.Intents, command_prefix: str, application_id: int
    ):
        super().__init__(
            intents=intents,
            command_prefix=command_prefix,
            application_id=application_id,
        )

    async def setup_hook(self):
        for extension in INSTALLED_EXTENSIONS:
            await self.load_extension(extension)
        bot.tree.copy_global_to(guild=DISCORD_GUILD)
        await bot.tree.sync(guild=DISCORD_GUILD)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


intents = discord.Intents.default()

bot = BotClient(
    intents=intents, command_prefix="=", application_id=settings.DISCORD_APPLICATION_ID
)


def run(token):
    print("[Bot] - Starting with DEBUG=" + str(settings.DEBUG))
    bot.run(token, reconnect=True)
