
import requests
import tweepy
import time
import random
import os

# Environment Variables
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
BUFFER_ACCESS_TOKEN = os.getenv('BUFFER_ACCESS_TOKEN')
BUFFER_PROFILE_IDS = os.getenv('BUFFER_PROFILE_IDS')  # Comma-separated profile IDs

last_video = ""

# Get the latest YouTube video
def get_latest_youtube_video():
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&order=date&part=snippet&type=video&maxResults=1"
    response = requests.get(url)
    data = response.json()
    latest_video_id = data['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={latest_video_id}"
    return video_url

# Post to Telegram
def post_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

# Post to Twitter
def post_to_twitter(message):
    auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(message)

# Post to Buffer (Instagram and Facebook)
def post_to_buffer(message):
    profile_ids = BUFFER_PROFILE_IDS.split(',')
    for profile_id in profile_ids:
        url = 'https://api.bufferapp.com/1/updates/create.json'
        payload = {
            'profile_ids[]': profile_id,
            'text': message,
            'access_token': BUFFER_ACCESS_TOKEN
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Posted to Buffer profile {profile_id} successfully.")
        else:
            print(f"Failed to post to Buffer profile {profile_id}. Response: {response.text}")

# Hashtag Generator
def generate_hashtags(topic):
    hashtags_bank = {
        'forex': ['#forex', '#forextrader', '#xauusd', '#forexsignals', '#goldtrading'],
        'youtube': ['#youtube', '#youtuber', '#newvideo', '#subscribe', '#watchnow'],
        'general': ['#trending', '#viral', '#explore', '#share', '#like']
    }
    return ' '.join(random.sample(hashtags_bank.get(topic, hashtags_bank['general']), 3))

# Main Automation Loop
while True:
    try:
        new_video = get_latest_youtube_video()
        if new_video != last_video:
            hashtags = generate_hashtags('youtube')
            message = f"🔥 New Video Alert! 🚀\nWatch now: {new_video}\n{hashtags}"

            post_to_telegram(message)
            post_to_twitter(message)
            post_to_buffer(message)

            print("New video posted to Telegram, Twitter, Instagram, and Facebook!")
            last_video = new_video
        else:
            print("No new video detected.")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(300)  # Check every 5 minutes
