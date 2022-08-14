from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from recipes.models import Recipes


@admin.action(description='Mark selected recipes as blocked')
def make_blocked(modeladmin, request, queryset):
    queryset.update(is_active=False, status='b')


@admin.action(description='Mark selected recipes as active')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True, status='a')


class RecipeInLine(TabularInline):
    model = Recipes
    fields = ['pk', 'access']
    readonly_fields = ['pk', 'access']
    extra = 0


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ['email']
    inlines = [
        RecipeInLine
    ]

    fieldsets = [
        (None, {
            'fields': ('first_name', 'last_name', 'city', 'description', 'total_recipe')
        })
    ]
    readonly_fields = ['first_name', 'last_name', 'city', 'description', 'total_recipe']
    list_display = ['first_name', 'last_name', 'city', 'total_recipe', 'status']
    search_fields = ['first_name', 'last_name']
    actions = [make_blocked, make_active]

    def total_recipe(self, obj):
        from django.db.models import Count
        result = Recipes.objects.filter(creator=obj).aggregate(Count('title'))
        return result['title__count']



admin.site.register(CustomUser, CustomUserAdmin)

