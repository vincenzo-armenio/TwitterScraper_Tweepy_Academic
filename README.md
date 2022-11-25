# Twitter Scraper

Search and download tweets from Twitter using Tweepy and Twitter API v.2. The code works with Twitter API Academic Research Access, which has a limit of 10 million tweets a month and allows full archive search, back to March 2006.




## Installation 
Install the libraries 

```bash
  pip install -r requirements.txt
```
    
## Authentication

Edit the twitter_authentication file with your bearer_token

bearer_token = "YOUR BEARER TOKEN HERE"

```javascript
from twitter_authentication import bearer_token

client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

```


## Building queries for Search Tweets

You also likely want to build a somewhat advanced query - instructions are at :
https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query


For this query, I get English language tweets that are not retweets.
```python
#enter the keyword
query = "#MeToo lang:en"

#enter filename of the dataset 
data_set_name = 'MeToo'

path = data_set_name + '.csv'

```
## Set Start_date and End_date

```python
#year, month, day
start_date = date(2021, 1, 20)
end_date = date(2021, 1, 21)

#this converts dates to the right format
start_date_conv = start_date.strftime("%Y-%m-%dT00:00:00Z")
end_date_conv   = end_date.strftime("%Y-%m-%dT00:00:00Z")

```

## Search Tweets

Full documentation for searching tweets is at https://docs.tweepy.org/en/latest/client.html#search-tweets.

By default the only information returned is the tweet ID and the text. Often, we will want information about authors, too. To get information about the author, you need to add the user_fields parameter with the fields you want as well as the expansions = 'author_id' parameter.

To get more information about the tweet, you need the tweet_fields parameter. The options are shown at https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all

```python

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

```

## Saves tweets to a csv file

We will often want to reorganize these into file, which means connecting a tweet to the user data of the user who wrote it. I show an example of how to do that here:

```python

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


```
