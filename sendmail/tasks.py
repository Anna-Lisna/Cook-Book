from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.template import Template, Context
from cookApp.celery import app
from recipes.models import Recipes
from users.models import CustomUser
from cook_app_drf.models import EmailForLetters


REPORT_TEMPLATE = """"
    {% for recipe in top_recipes %}
        '{{ recipe.title }}: likes {{ recipe.total_likes }}, comments {{recipe.total_comments}}
    {% endfor %}
  """

RECIPE_TEMPLATE = """
    {{ recipe.title }}
    {{ recipe.ingredients }}
    {{ recipe.description }}
"""


@app.task
def send_top_5_recipes():
    top_recipes = Recipes.active.filter(access='public').annotate(num_l=Count('likes'), num_c=Count('comments')).order_by('-num_l', '-num_c')
    template = Template(REPORT_TEMPLATE)
    subject = 'Top 5 recipe'
    message = template.render(context=Context({'top_recipes': top_recipes[:5]}))
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email for user in CustomUser.objects.all()]
    send_mail(subject, message, email_from, recipient_list)
    return "Mail has been sent........"


@shared_task
def send_change_access_recipe(id):
    template = Template(RECIPE_TEMPLATE)
    subject = 'New recipe'
    message = template.render(context=Context({'recipe': Recipes.active.get(id=id)}))
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email for email in EmailForLetters.objects.all()]
    send_mail(subject, message, email_from, recipient_list)
    return "Mail has been sent........"
