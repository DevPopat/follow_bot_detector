'''This project requires the use of the Twitter API (Tweepy).
This project is able to detect up to 40 follow-bots for a given Twitter account.
Applies Python and Eclipse IDE to design the program
'''

import tweepy
import time
import datetime

# Access codes from Twitter

consumerkey = ''

consumersecret = ''

accesstoken = ''

accesstokensecret = ''


# Create API handle

auth = tweepy.OAuthHandler(consumerkey, consumersecret)

auth.set_access_token(accesstoken, accesstokensecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Use this between network calls to avoid hitting the API limit
time.sleep(60)

#function to get the followers 
def get_followers(user_name):
    #empty object list
    object_list = []
    #to get all the followers of the account
    followers = api.followers(user_name)
    #iterate through information about each follower and add them to the object list
    count = 0

#this loop is to prevent the program from hitting a rate limit. 
    for f in followers:
        #break after reaching 15 followers 
        if count == 15:
            break
        object_list.append(f)
        #increment count by 1 after each follower
        count += 1
    return object_list

#function to find a follow bot 
def find_bot(user):
    is_bot = False
    high_followers = False 
    #set a start date
    start = datetime.datetime.now() - datetime.timedelta(days = 15)
    #set an end date (today, right now)
    end = datetime.datetime.now()
    #split the elements of the list with the dates when the twitter profile of the followers were created 
    date_list = str(user.created_at).split()
    date_list = date_list[0].split('-')
    #day the 2nd index of date_list
    #month is the first index of date_list 
    #year is the 0th index of date_list 
    date = datetime.datetime(day = int(date_list[2]), month = int(date_list[1]), year = int(date_list[0]))
    #to get the number of profiles following the user
    num_user_is_following = len(user.followers_ids(user.screen_name))  
    #to get the number of profiles the user is following 
    user_following = api.friends_ids(user.screen_name)
    #iterating through those followers
    #if any of those profiles have more than 20,000 followers
    for i in user_following:
        if api.get_user(i).followers_count > 20000:
            #change high followers to True 
            high_followers = True
            break
    
    #print the name of the user (inputed user's followers)
    print("Examining @{}...".format(user.screen_name))
    if high_followers == False:
        is_bot = False
    else:
        #conditions to detect a follow-bot 
        if (0 <= user.followers_count < 10 and 0 <= num_user_is_following < 50 and 0 <= user.statuses_count < 20 and start <= date <= end and 
            user.profile_image_url == 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'):
            is_bot = True
    return is_bot
                    

if __name__ == '__main__':
    #to input the twitter username
    user_name = input("input user name here: ")
    #set bot count equal to 0 and later increment it as each bot is detected 
    bot_count = 0
    #gives me the object of the user containing all their data
    user = api.get_user(user_name)
    followers_list = get_followers(user_name)
    #for each follower in a given user's list of followers 
    for follower in followers_list:
        #if the follower is a bot
        x = find_bot(follower)
        if x == True:
            #increment bot count by 1
            bot_count += 1
            #print that your code has detected a bot 
            print("Found follow-bot #{}: twitter.com/{}".format(bot_count, follower.screen_name))