from recipes.models import Recipes


class Dashboard(Recipes):
    class Meta:
        proxy = True
