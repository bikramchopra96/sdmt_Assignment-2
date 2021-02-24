from django.db import models

# Create your models here.
class TwitterModel(models.Model):
    tweetId = models.CharField(max_length = 20)
    created_at = models.DateTimeField()
    added_at = models.DateTimeField(auto_now_add=True,auto_now=False)
    tweet = models.CharField(max_length = 280)


class RedditModel(models.Model):
    title = models.CharField(max_length = 100)
    created_at = models.DateTimeField()
    added_at = models.DateTimeField(auto_now_add=True,auto_now=False)
    post = models.CharField(max_length = 280)