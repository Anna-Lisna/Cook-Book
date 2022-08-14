from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count
from django.db.models.functions import Extract, TruncWeek

from .models import Dashboard
from users.models import CustomUser
from recipes.models import Recipes
from datetime import datetime


class DashboardAdmin(admin.ModelAdmin):
    change_list_template = 'admin/dashboard_change_list.html'

    def get_total_users(self):
        total = CustomUser.objects.all().count()
        return total

    def get_total_users_last_week(self):
        current_week = datetime.now().isocalendar()[1]
        last_week = current_week - 1
        all_users = CustomUser.objects.all()
        total = 0

        for i in all_users:
            if i.date_joined.isocalendar()[1] == last_week:
                total += 1

        return total


    def get_public_recipes(self):
        total = Recipes.objects.filter(access='public').count()
        return total

    def get_private_recipes(self):
        total = Recipes.objects.filter(access='private').count()
        return total

    def get_total_likes(self):
        total = Recipes.objects.all().aggregate(tot=Count('likes'))['tot']
        return total

    def get_total_comments(self):
        total = Recipes.objects.all().aggregate(tot=Count('comments'))['tot']
        return total

    def changelist_view(self, request, extra_context=None):
        my_context = {
            'total_users': self.get_total_users(),
            'total_users_last_week': self.get_total_users_last_week(),
            'total_public_recipes': self.get_public_recipes(),
            'total_private_recipes': self.get_private_recipes(),
            'total_likes': self.get_total_likes(),
            'total_comments': self.get_total_comments()

        }
        return super(DashboardAdmin, self).changelist_view(request, extra_context=my_context)


admin.site.register(Dashboard, DashboardAdmin)
admin.site.unregister(Group)
