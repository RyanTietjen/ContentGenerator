"""
Ryan Tietjen
Jan 2024
Simple program to produce short-form content for tiktok/youtube shorts.
You must fill out the config file in order for this program to work.
More information can be found at https://github.com/RyanTietjen/ContentGenerator
"""

import praw  # Reddit API; used to get posts
from pathlib import Path # Used for storing/loading assets and final videos
import configparser  # Used in conjunction with the config file
from text_setup import get_text
from generate_tts import text_to_speech
from generate_subtitles import generate_subtitles
from produce_video import produce_final_video
          
# Sets up config file
config = configparser.ConfigParser()
config.read('config.ini')

#Establishes read/write Paths
assets_path = Path(config["Data Storage"]["assets_path"])
results_path = Path(config["Data Storage"]["results_path"])
temp_audio_path = assets_path / "output.mp3"
background_video_path = assets_path / "background.mp4"

# links to reddit
reddit = praw.Reddit(
    client_id=config["Reddit"]["client_id"],
    client_secret=config["Reddit"]["client_secret"],
    user_agent=config["Reddit"]["user_agent"],
)
subreddit = reddit.subreddit(config["Reddit"]["subreddit"])

#1. Obtain the text
post_title_and_text = get_text(config, reddit)

# Repeat the following process for each post
for i, post in enumerate(post_title_and_text, start=1):
    #2. Generate TTS
    full_text = ' '.join(post)
    text_to_speech(full_text[:2998], config, temp_audio_path)
    
    #3. Generate subtitles
    subtitles = generate_subtitles(temp_audio_path)
    
    #4. Produce the final video
    produce_final_video(post[0], 
                        subtitles, 
                        temp_audio_path, 
                        background_video_path, 
                        assets_path,
                        config)
    
