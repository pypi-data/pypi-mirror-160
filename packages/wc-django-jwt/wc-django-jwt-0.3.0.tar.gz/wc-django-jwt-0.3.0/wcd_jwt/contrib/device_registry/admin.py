from django.contrib import admin

from .models import TokenInterlocutorConnection


@admin.register(TokenInterlocutorConnection)
class TokenInterlocutorConnectionAdmin(admin.ModelAdmin):
    list_display = 'id', 'interlocutor', 'token', 'created_at',
    date_hierarchy = 'created_at'
    list_select_related = 'interlocutor', 'token',
    autocomplete_fields = 'interlocutor', 'token',
    search_fields = 'id', 'interlocutor__user_agent', 'token__token', 'token__jti',
