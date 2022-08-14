from django.contrib import admin
from .models import Recipes


@admin.action(description='Mark selected recipes as blocked')
def make_blocked(modeladmin, request, queryset):
    queryset.update(status='b')


@admin.action(description='Mark selected recipes as active')
def make_active(modeladmin, request, queryset):
    queryset.update(status='a')


class RecipeAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'image', 'access', 'creator', 'total_likes', 'total_comments']
    list_display = ['title', 'short_description', 'creator', 'create_date', 'total_likes', 'total_comments', 'status']
    readonly_fields = ['creator', 'total_likes', 'total_comments']
    search_fields = ['title']
    list_filter = ['creator']
    actions = [make_blocked, make_active]

    class Meta:
        model = Recipes


admin.site.register(Recipes, RecipeAdmin)
