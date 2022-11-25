import random
import tweepy
from datetime import date
from twitter_authentication import bearer_token
from time import sleep
import pandas as pd
from random import randint

client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

query = "#meloni -is:retweet lang:en"

data_set_name = 'Meloni'

path = data_set_name + '.csv'

start_date = date(2021, 1, 20)
end_date = date(2021, 1, 21)

start_date_conv = start_date.strftime("%Y-%m-%dT00:00:00Z")
end_date_conv   = end_date.strftime("%Y-%m-%dT00:00:00Z")

tweets_list = []

for response in tweepy.Paginator(client.search_all_tweets, 
                                    query = query,
                                    user_fields = ['username', 'public_metrics', 'description', 'location'],
                                    tweet_fields = ['created_at', 'geo', 'public_metrics', 'text'],
                                    expansions = 'author_id',
                                    start_time = start_date_conv,
                                    end_time = end_date_conv,
                                    max_results=500,   
                                ):

                sleeptime = random.uniform(1,2)
                print("API REQUEST")
                print("sleeping for:", sleeptime, "seconds") 
                sleep(sleeptime)
                print("DOWNLOAD...")
                tweets_list.append(response)

result = []
user_dict = {}
            
for response in tweets_list:
          
    
    for user in response.includes['users']:
        user_dict[user.id] = {'username': user.username, 
                              'followers': user.public_metrics['followers_count'],
                              'tweets': user.public_metrics['tweet_count'],
                              'description': user.description,
                              'location': user.location
                             }

    for tweet in response.data:
        
        author_info = user_dict[tweet.author_id]
        
        result.append({ 
                       'author_id': tweet.author_id, 
                       'username': author_info['username'],
                       'author_followers': author_info['followers'],
                       'author_tweets': author_info['tweets'],
                       'author_description': author_info['description'],
                       'author_location': author_info['location'],
                       'text': tweet.text,
                       'created_at': tweet.created_at,
                       'retweets': tweet.public_metrics['retweet_count'],
                       'replies': tweet.public_metrics['reply_count'],
                       'likes': tweet.public_metrics['like_count'],
                       'quote_count': tweet.public_metrics['quote_count']
                    })
            
    df = pd.DataFrame(result)
            
    df.to_csv(path)

