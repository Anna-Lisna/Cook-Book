from django.db import models


class EmailForLetters(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f'{self.email}'
