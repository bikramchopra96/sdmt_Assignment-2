from django.contrib import admin
from .models import TwitterModel,RedditModel
# Register your models here.
class TwitterAdmin(admin.ModelAdmin):
    #'Action_taken_at',
    list_display = ('added_at','created_at','tweetId', 'tweet')
    ordering = ('created_at', 'tweetId')


class RedditAdmin(admin.ModelAdmin):
    #'Action_taken_at',
    list_display = ('added_at','created_at','title', 'post')
    ordering = ('created_at', 'title')


admin.site.register(TwitterModel,TwitterAdmin)
admin.site.register(RedditModel,RedditAdmin)