import discord
from discord import app_commands
from django.conf import settings

DISCORD_GUILD = discord.Object(id=settings.DISCORD_GUILD_ID)


class BotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, application_id: int):
        super().__init__(intents=intents, application_id=application_id)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=DISCORD_GUILD)
        await self.tree.sync(guild=DISCORD_GUILD)


intents = discord.Intents.default()

client = BotClient(intents=intents, application_id=settings.DISCORD_APPLICATION_ID)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


def run(token):
    print("[Bot] - Starting with DEBUG=" + str(settings.DEBUG))
    client.run(token, reconnect=True)


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")
