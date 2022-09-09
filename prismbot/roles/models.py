from django.db import models


class RoleCategory(models.Model):
    name = models.CharField(
        max_length=200, help_text="The plain-language identifier of the Category"
    )
    message = models.TextField(
        blank=True,
        default="",
        help_text="Text to use for the role signup message explaining the purpose of the Category",
    )
    self_assignable = models.BooleanField(
        default=False,
        help_text="Whether the bot should allow self-assignment of roles in this Category",
    )
        unique = models.BooleanField(
        default=False,
        help_text="Set to TRUE if only one role in this category may be active at a time",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "role categories"


class DiscordRole(models.Model):
    discord_role_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="The unique Discord object ID for the Role",
    )
    name = models.CharField(
        max_length=200, help_text="The name assigned to the Role in Discord"
    )
    emoji = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default="",
        help_text="Emoji (unicode or discord emoji <name:id> tag) to associate with the Role; appears on signup buttons",
    )
    category = models.ForeignKey(
        RoleCategory,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="discord_roles",
    )

    def __str__(self):
        return self.name
