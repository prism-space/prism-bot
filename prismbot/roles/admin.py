from django.contrib import admin

from .models import DiscordRole, RoleCategory


@admin.register(DiscordRole)
class DiscordRoleAdmin(admin.ModelAdmin):
    model = DiscordRole
    list_display = ("name", "emoji", "category")


@admin.register(RoleCategory)
class RoleCategoryAdmin(admin.ModelAdmin):
    model = RoleCategory
    list_display = ("name", "message", "self_assignable")
