from django.contrib import admin

from .models import Token, TokenUserConnection


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = 'id', 'jti', 'parent_id', 'expired_at', 'created_at',
    date_hierarchy = 'created_at'
    autocomplete_fields = 'parent',
    search_fields = 'id', 'jti', 'token',


@admin.register(TokenUserConnection)
class TokenUserConnectionAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'token', 'created_at',
    date_hierarchy = 'created_at'
    list_select_related = 'user', 'token',
    autocomplete_fields = 'user', 'token',
    search_fields = 'id', 'user__username', 'token__token', 'token__jti',
