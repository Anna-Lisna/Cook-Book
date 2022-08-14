from django.db import models
from recipes.models import Recipes
from users.models import CustomUser


class Comment(models.Model):
    recipe = models.ForeignKey(Recipes, related_name='comments', on_delete=models.CASCADE)
    creator = models.ForeignKey(CustomUser, related_name='creator', on_delete=models.CASCADE)
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.recipe.title, self.creator)

