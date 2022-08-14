from django.db import models
from django.urls import reverse
from users.models import CustomUser


STATUS_CHOICES = [
    ('a', 'Active'),
    ('b', 'Block')
]

ACCESS_CHOICES = [
    ('public', 'public'),
    ('private', 'private')
]


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status='b')


class Images(models.Model):
    images = models.FileField(upload_to='static/img/blog-img')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='creator_images')

    def __str__(self):
        return f'{self.images}'


class Recipes(models.Model):
    objects = models.Manager()
    active = ActiveManager()
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    description = models.TextField()
    image = models.ForeignKey(Images, on_delete=models.CASCADE, related_name='image_recipe')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='creator_recipe')
    create_date = models.DateField(auto_now_add=True)
    access = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='private')
    likes = models.ManyToManyField(CustomUser, related_name='recipe_likes')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def short_description(self):
        return self.description[:25]

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def image_url(self):
        return self.image.images.url

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('recipe_detail', args=(str(self.id)))






