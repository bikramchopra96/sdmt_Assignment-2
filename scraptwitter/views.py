from django.shortcuts import render,redirect
from .cred import keys,redit_keys
from .models import TwitterModel,RedditModel
import tweepy
from django.db.models import Max
import datetime
import praw
# Create your views here.
def home(request):
    return render(request, 'specific_home.html')

def TwitterShowData(request):
    TESTING = False
    if not TESTING:
        #----------Authenticating webapp with Twitter-------------
        consumer_key = keys["API key"]
        consumer_secret = keys["API key secret"]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(keys['Access token'], keys['Access token secret'])
        api = tweepy.API(auth)

        #-----------Getting posts from twitter---------
        tweets = api.user_timeline(screen_name=keys["userID"],
                                   count=200,
                                   include_rts=False,
                                   tweet_mode='extended'
                                   )
        latestdate = TwitterModel.objects.aggregate(Max('created_at'))['created_at__max']
        print(latestdate)
        for info in tweets:
            # current_date = dt.datetime.strptime(info.created_at, '%Y-%m-%d %H:%M:%S')
            current_date = info.created_at
            if(latestdate != None):
                if(current_date > latestdate):
                    instance = TwitterModel()
                    instance.tweetId = str(info.id)
                    instance.created_at = info.created_at
                    instance.tweet = info.full_text
                    instance.save()
                    print("data to added to db ", info.id,info.created_at,info.full_text)
            else:
                instance = TwitterModel()
                instance.tweetId = str(info.id)
                instance.created_at = info.created_at
                instance.tweet = info.full_text
                instance.save()
                print("data to added to db ", info.id, info.created_at, info.full_text)
    tweets = TwitterModel.objects.all().order_by('-created_at')
    return render(request, 'tweetshowGUI.html',{'records':tweets})

def TwitterPostData(request):
    if (request.method == 'POST'):
        data = request.POST
        print(data,data['tweet'])
        # ----------Authenticating webapp with Twitter-------------
        consumer_key = keys["API key"]
        consumer_secret = keys["API key secret"]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(keys['Access token'], keys['Access token secret'])
        api = tweepy.API(auth)
        api.update_status(data['tweet'])
        return redirect('/tshow/')

    return render(request, "tweetpost.html")


def RedditShowData(request):
    posts = RedditModel.objects.all().order_by('-created_at')
    return render(request, 'postshowGUI.html',{'records':posts})

def RedditPostData(request):
    if (request.method == 'POST'):
        data = request.POST
        print(data,data['title'],data['post'])
        TESTING = False
        if not TESTING:
            # Authenticating with reddit
            reddit = praw.Reddit(client_id=redit_keys['client_id'],
                                 client_secret=redit_keys['client_secret'],
                                 user_agent=redit_keys['user_agent'],
                                 redirect_uri=redit_keys['redirect_uri'],
                                 refresh_token=redit_keys['refresh_token'])

            subr = 'pythonsandlot'
            subreddit = reddit.subreddit(subr)
            title = data['title']
            selftext = data['post']
            reddit.validate_on_submit = True
            print(subreddit.submit(title, selftext=selftext))

        #-------Saving the post to db---------
        instance = RedditModel()
        instance.title = data['title']
        instance.post = data['post']
        instance.created_at = datetime.datetime.now()
        instance.save()
        print('Saved to db')
        return redirect('/rshow/')

    return render(request, "rpost.html")