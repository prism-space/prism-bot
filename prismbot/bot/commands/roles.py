import logging
from enum import Enum
from functools import partial
from typing import Coroutine, Dict, List, Tuple

import discord
from asgiref.sync import sync_to_async
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

from prismbot.roles.models import DiscordRole, RoleCategory

logger = logging.getLogger()


class RoleButtonStyle(Enum):
    ASSIGNED = discord.ButtonStyle.success.value
    UNASSIGNED = discord.ButtonStyle.secondary.value


class RoleAssignmentButton(Button):
    def __init__(self, role: DiscordRole, member: discord.Member) -> None:
        role_id = role.discord_role_id
        style = (
            RoleButtonStyle.ASSIGNED
            if self.member_has_role(member, role)
            else RoleButtonStyle.UNASSIGNED
        )
        super().__init__(
            style=style, label=role.name, custom_id=str(role_id), emoji=role.emoji
        )

    async def callback(self, interaction: discord.Interaction):
        member, role = self.interaction_member_and_role(interaction)
        has_role = self.member_has_role(member, role)
        try:
            if has_role:
                await member.remove_roles(
                    role, reason="Member removed role from themself"
                )
                self.style = RoleButtonStyle.UNASSIGNED
                logger.info(f"Removed role {role.name} from {member.display_name}")
            else:
                await member.add_roles(role, reason="Member self-assigned role")
                self.style = RoleButtonStyle.ASSIGNED
                logger.info(f"Added role {role.name} to {member.display_name}")
        except (discord.errors.Forbidden, discord.errors.HTTPException) as error:
            logger.error(f"Role assignment error: {error}")
            return await interaction.response.send_message(
                "I couldn't handle that for some reason. Could you try again?",
                ephemeral=True,
            )
        return await interaction.response.edit_message(view=self.view)

    def interaction_member_and_role(
        self, interaction: discord.Interaction
    ) -> Tuple[discord.Member, discord.Role]:
        roles_by_id = self.guild_roles_by_id(interaction.guild.roles)
        guild_role = roles_by_id.get(self.role_id())
        return (interaction.user, guild_role)

    def member_has_role(self, member, role) -> bool:
        return role in member.roles

    def guild_roles_by_id(self, guild_roles) -> Dict[str, discord.Role]:
        return {role.id: role for role in guild_roles}

    def role_id(self) -> str:
        return int(self.custom_id)


class RoleAssignmentView(View):
    def __init__(
        self,
        category: RoleCategory,
        member: discord.Member,
        interaction: discord.Interaction,
        timeout_callback: Coroutine,
    ) -> None:
        super().__init__(timeout=300)
        self.member = member
        self.interaction = interaction
        self.timeout_callback = timeout_callback
        self.populate(category, member)

    def populate(self, category, member):
        for role in category.discord_roles.all():
            self.add_item(RoleAssignmentButton(role, member))

    async def on_timeout(self) -> None:
        logger.info(f"Timing out role view called by {self.member.display_name}")
        await self.timeout_callback()
        return await super().on_timeout()


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @sync_to_async(thread_sensitive=False)
    def get_assignable_categories(self) -> List[RoleCategory]:
        return list(
            RoleCategory.objects.filter(self_assignable=True)
            .order_by("name")
            .prefetch_related("discord_roles")
        )

    @app_commands.command(
        name="roles", description="Opens the role self-assignment dialogues"
    )
    async def roles(self, interaction: discord.Interaction):
        await interaction.response.send_message("Fetching roles...", ephemeral=True)
        assignable_categories = await self.get_assignable_categories()
        category_messages = []
        clear_callback = partial(self.clear_messages, category_messages, interaction)
        for category in assignable_categories:
            category_view = RoleAssignmentView(
                category=category,
                member=interaction.user,
                interaction=interaction,
                timeout_callback=clear_callback,
            )
            category_webhook: discord.WebhookMessage = await interaction.followup.send(
                category.message, view=category_view, ephemeral=True
            )
            await interaction.edit_original_message(
                content="Role self-assignment options:"
            )
            category_messages.append(category_webhook)

    async def clear_messages(
        self, messages: List[discord.WebhookMessage], interaction: discord.Interaction
    ):
        for message in messages:
            try:
                await message.edit(content="Menu expired.", view=None)
                await interaction.edit_original_message(
                    content="The role menus have expired. Don't worry! Your changes have been saved. Type '/roles' again to reopen."
                )
            except Exception as error:
                logger.warning(f"WebhookMessage deletion failed. Reason: {error}")

    @app_commands.command(
        name="refresh-roles", description="Add existing roles to PrismBot's memory"
    )
    async def refresh_roles(self, interaction: discord.Interaction):
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
