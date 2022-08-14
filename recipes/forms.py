from django import forms
from .models import Recipes, Images


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipes
        fields = ['title', 'ingredients', 'description', 'image', 'access']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'access': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, user=None, **kwargs):
        super(RecipeForm, self).__init__(**kwargs)
        if user:
            self.fields['image'].queryset = Images.objects.filter(creator=user)
