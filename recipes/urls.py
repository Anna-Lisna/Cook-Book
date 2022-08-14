from django.urls import path
from .views import RecipesList, RecipeDetail, RecipeCreate, RecipeUpdate, RecipeLikes


urlpatterns = [
    path('', RecipesList.as_view(), name='home'),
    path('recipes/<int:pk>', RecipeDetail.as_view(), name='recipe_detail'),
    path('add_recipe', RecipeCreate.as_view(), name='add_recipe'),
    path('recipes/edit/<int:pk>', RecipeUpdate.as_view(), name='update_recipe'),
    path('like/<int:pk>', RecipeLikes, name='recipe_like')
]

