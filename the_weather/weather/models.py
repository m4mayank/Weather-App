from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'countries'


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=30)
    slug = models.SlugField(allow_unicode=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SelectedCity(models.Model):
    city = models.ForeignKey(City, related_name='selected_city', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)

    def __str__(self):
        return (self.user.username+"_"+self.city.name)

    class Meta:
        verbose_name_plural = 'selectedcities'
        unique_together = ('city','user')