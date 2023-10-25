from django.db import models
from news.models import News

class Link(models.Model):
    token = models.CharField(max_length=12, unique=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return self.token