from django.urls import path
from .views import CommentCreate


urlpatterns = [
    path('recipes/<int:pk>/comment', CommentCreate.as_view(), name="add_comment")
]

