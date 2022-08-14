from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Recipes
from .forms import RecipeForm


class RecipesList(ListView):
    paginate_by = 6
    model = Recipes
    queryset = Recipes.active.filter(access='public', creator__status='a')
    template_name = 'recipes/home.html'
    ordering = ['-create_date']


def RecipeLikes(request, pk):
    recipe = get_object_or_404(Recipes, id=request.POST.get('recipe_id'))
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return HttpResponseRedirect(reverse('recipe_detail', args=[str(pk)]))


class RecipeDetail(DetailView):
    model = Recipes
    template_name = 'recipes/recipe.html'

    def get_context_data(self, **kwargs):
        context_data = super(RecipeDetail, self).get_context_data(**kwargs)

        likes_recipe = get_object_or_404(Recipes, id=self.kwargs['pk'])

        liked = False
        if likes_recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        context_data['total_likes'] = likes_recipe.total_likes()
        context_data['recipe_is_liked'] = liked
        context_data['total_comments'] = likes_recipe.total_comments()
        return context_data


class RecipeCreate(CreateView):
    model = Recipes
    form_class = RecipeForm
    template_name = 'recipes/add_recipe.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.image__creator = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user
        return kwargs


class RecipeUpdate(UpdateView):
    model = Recipes
    form_class = RecipeForm
    template_name = 'recipes/update_recipe.html'



