from django.contrib import admin

from rotations.models import Member, Rotation


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin config for the Event model."""
    search_fields = ('name', 'email')
    list_display = ('name', 'email')

    fields = ('name', 'email', 'created', 'modified')
    readonly_fields = ('created', 'modified')


@admin.register(Rotation)
class RotationAdmin(admin.ModelAdmin):
    """Admin config for the Subscriber model."""
    search_fields = ('name',)
    list_display = ('name', 'description', 'on_call')

    fields = ('name', 'description', 'message', 'members', 'on_call', 'created', 'modified')
    readonly_fields = ('created', 'modified')
