from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('register/', GetAuthToken.as_view()),
    path('login/', obtain_auth_token),
    path('users/', AllUsers.as_view(), name='users'),
    path('update-user/<int:id>/', UpdateUser.as_view({'get': 'retrieve'})),
    path('user-recipes/', UserRecipe.as_view({'get': 'list'})),
    path('update_recipes/<int:id>/', UpdateRecipe.as_view({'get': 'retrieve'}))
]

router = routers.SimpleRouter()
router.register(r'add-recipe', CreateRecipe, basename='add_recipe')
router.register(r'add-image', LoadImage, basename='add_image')
router.register(r'recipes', RecipesPublic, basename='recipes')
router.register(r'user', UserProfile)
router.register(r'receive_letters', ReceiveLetters, basename='receive_letters')
