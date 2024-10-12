import tweepy
import yaml
from flask import Flask, render_template, request, jsonify
from collections import defaultdict
from judge_learning import judge_political_leaning
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the bearer token from the yaml file
try:
    with open('/Users/nicholasflores/Documents/Secrets/xai.yaml', 'r') as file:
        config = yaml.safe_load(file)
        bearer_token = config['x']['bearer']
except Exception as e:
    logging.error(f"Error loading config: {str(e)}")
    raise

# Authenticate using the bearer token
try:
    client = tweepy.Client(bearer_token=bearer_token)
except Exception as e:
    logging.error(f"Error authenticating with Twitter: {str(e)}")
    raise

# Function to pull the last n tweets for a single account
def get_last_n_tweets_for_account(account, n):
    tweets = []
    
    try:
        # Get user ID for the Twitter handle
        user = client.get_user(username=account)
        user_id = user.data.id

        # Pull the last n tweets from that user
        response = client.get_users_tweets(
            id=user_id,
            max_results=n,
            tweet_fields=['created_at', 'text']
        )

        if response.data:
            for tweet in response.data:
                tweets.append({
                    'username': account,
                    'created_at': tweet.created_at,
                    'text': tweet.text,
                    'id': tweet.id
                })
    except Exception as e:
        logging.error(f"Error fetching tweets for {account}: {str(e)}")
    
    return tweets

# Function to pull the last n tweets from multiple accounts
def get_last_n_tweets_from_accounts(accounts, n):
    all_tweets = []
    for account in accounts:
        tweets = get_last_n_tweets_for_account(account, n)
        all_tweets.extend(tweets)
    return all_tweets

@app.route('/')
def home():
    return render_template('xaiHackHome.html')

@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    if request.method == 'POST':
        try:
            accounts = request.form.get('accounts').split(',')
            n_tweets = int(request.form.get('n_tweets', 10))  # Default to 10 tweets if not specified
            
            tweets = get_last_n_tweets_from_accounts(accounts, n_tweets)
            
            # Organize tweets by user
            tweets_by_user = defaultdict(list)
            for tweet in tweets:
                tweets_by_user[tweet['username']].append({
                    'username': tweet['username'],
                    'created_at': tweet['created_at'].isoformat(),
                    'text': tweet['text'],
                    'id': tweet['id']
                })
            
            return jsonify(dict(tweets_by_user))
        except Exception as e:
            logging.error(f"Error in lookup route: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    return render_template('lookup.html')

@app.route('/singletweet', methods=['GET', 'POST'])
def singletweet():
    if request.method == 'POST':
        try:
            tweet_content = request.json.get('tweetContent')
            if not tweet_content:
                return jsonify({"error": "No tweet content provided"}), 400
            
            analysis = judge_political_leaning(tweet_content)
            return jsonify({"analysis": analysis})
        except Exception as e:
            logging.error(f"Error in singletweet route: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    return render_template('singletweet.html')

@app.route('/analyze_tweet', methods=['POST'])
def analyze_tweet():
    try:
        tweet_content = request.json.get('tweetContent')
        if not tweet_content:
            return jsonify({"error": "No tweet content provided"}), 400
        
        analysis = judge_political_leaning(tweet_content)
        return jsonify({"analysis": analysis})
    except Exception as e:
        logging.error(f"Error in analyze_tweet route: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
