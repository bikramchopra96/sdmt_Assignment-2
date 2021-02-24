from django.contrib import admin
from .models import TwitterModel
# Register your models here.
class TwitterAdmin(admin.ModelAdmin):
    #'Action_taken_at',
    list_display = ('added_at','created_at','tweetId', 'tweet')
    ordering = ('created_at', 'tweetId')

admin.site.register(TwitterModel,TwitterAdmin)