from django.db import models
from django.utils.text import slugify


class Currency(models.Model):
    code = models.CharField(max_length=3)
    slug = models.SlugField()

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.slug = slugify(self.code)
        super().save(*args, **kwargs)
