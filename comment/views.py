from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .models import Comment
from .forms import CommentForm


class CommentCreate(CreateView):
    model = Comment
    template_name = 'comment/add_comment.html'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.recipe_id = self.kwargs['pk']
        form.instance.creator = self.request.user
        return super().form_valid(form)



