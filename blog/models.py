from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User



# Create your models here.
class Scraping(models.Model):

    url = models.URLField(max_length=300, unique=True)
    extracted_data = models.TextField(blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=0)

    def __str__(self):
        return self.url


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    visibility_choice = (
        (1, 'Public'),
        (2, 'Private'),
    )
    visibility = models.IntegerField(choices=visibility_choice, default=1)
    image = models.ImageField(default="default.jpg", upload_to='posts')

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})