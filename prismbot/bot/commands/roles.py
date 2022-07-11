import discord
from discord import app_commands
from discord.ext import commands

from prismbot.roles.models import DiscordRole


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="load-roles", description="Add existing roles to PrismBot's memory"
    )
    async def load_roles(self, interaction: discord.Interaction):
        guild_roles = interaction.guild.roles
        roles_to_create = [
            DiscordRole(discord_role_id=role.id, name=role.name) for role in guild_roles
        ]
        created_or_updated_roles = await DiscordRole.objects.abulk_create(
            roles_to_create,
            ignore_conflicts=True,
        )
        await interaction.response.send_message(
            f"Loaded {len(created_or_updated_roles)} roles.", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Roles(bot))
