# Ryan Tietjen
# Jan 2024
# Simple program to produce short-form content for tiktok/youtube shorts.
# You must fill out the config file in order for this program to work.
# More information can be found at https://github.com/RyanTietjen/ContentGenerator

import random  # used to get a random point from the background video
import re # Used to edit file text
import praw  # Reddit API; used to get posts
from boto3 import Session  # AWS Polly client; used for TTS
from moviepy.editor import *  # Produces the final video
import configparser  # Used in conjunction with the config file
import whisper_timestamped  # Used to generate subtitles
import ffmpeg # must be installed


# main function to generate posts.
def get_posts():
    # case we are using a link to a post
    if config["Settings"].getboolean("single_link"):
        # Fetch the submission
        single_post = reddit.submission(url=config["Settings"]["post_link"])
        single_post_text = single_post.title + single_post.selftext
        single_post_text = single_post_text.replace("AITA", "A.I.T.A")

        # Produce TTS and video
        text_to_speech(single_post_text)
        produce_final_video(single_post.title)
    # case we are taking the top # of posts from a certain time
    else:
        counter = 1

        # Fetch posts
        post_limit = int(config["Reddit"]["limit"])
        top_posts = subreddit.top(time_filter=config["Reddit"]["time_filter"], limit=post_limit)
        for post in top_posts:
            # Generates output
            print(f"GENERATING VIDEO {counter}/{post_limit}")
            full_text = post.title + post.selftext
            full_text = full_text.replace("AITA", "A.I.T.A")

            text_to_speech(full_text)
            subtitles = generate_subtitles()
            produce_final_video(post.title, subtitles)
            counter += 1


# Generates subtitles
def generate_subtitles():
    print("GENERATING SUBTITLES")
    subtitles = []

    model = whisper_timestamped.load_model("base")
    audio = "output.mp3"
    results = whisper_timestamped.transcribe(model, audio)

    for segment in results["segments"]:
        for word in segment["words"]:
            subtitles.append({"text": word["text"],
                              "start": float(word["start"]),
                              "end": float(word["end"])})

    return subtitles


# Produces tts
def text_to_speech(text, output_format='mp3', voice_id='Matthew'):
    print("GENERATING TTS")
    session = Session(aws_access_key_id=config["AWS"]["aws_access_key_id"],
                      aws_secret_access_key=config["AWS"]["aws_secret_access_key"],
                      region_name='us-east-1').client("polly")

    response = session.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    # Save audio to a file
    with open('output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())


# Generates random timestamps for the background video.
def generate_random_clip_timestamps(duration, audio_duration):
    max_start = int(duration - audio_duration)  # Maximum start point for the clip
    start_time = int(random.randint(0, max_start))  # Randomly select a start time
    end_time = int(start_time + audio_duration)  # Calculate end time based on audio duration
    return start_time, end_time


# Splits the title text into lines so that it fits within the specified width.
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    line = []

    # Create a TextClip for measuring text width
    for word in words:
        # Check the width of the line with the new word added
        line_plus_word = ' '.join(line + [word])
        text_clip = TextClip(line_plus_word, font=font, fontsize=80)
        text_width, _ = text_clip.size

        # If the line is too wide, start a new line
        if text_width > max_width:
            lines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)

    # Add the last line
    lines.append(' '.join(line))
    return '\n'.join(lines)


# Combines all parts of the video into the final result
def produce_final_video(title, subtitles):
    print("GENERATING VIDEO")
    tts = AudioFileClip("output.mp3")
    new_tts = CompositeAudioClip([tts])

    video = VideoFileClip("background.mp4")

    start, end = generate_random_clip_timestamps(video.duration, tts.duration)

    video = video.subclip(start, end)
    video.audio = new_tts

    # Produces the r/subreddit text seen in the thumbnail.
    subreddit_text = TextClip("r/" + str(config["Reddit"]["subreddit"]),
                              fontsize=110,
                              color='white',
                              font='Arial-Bold',
                              stroke_color='black',
                              stroke_width=4)

    subreddit_text = subreddit_text.set_position(("center", 0.1), relative=True).set_duration(4.5)

    # Produces the title text seen in the thumbnail.
    wrapped_title = wrap_text(title, "Arial-Bold", max_width=1000)

    post_title = TextClip(wrapped_title,
                          fontsize=80,
                          color='white',
                          font='Arial-Bold',
                          stroke_color='black',
                          interline=-22,
                          stroke_width=3)

    post_title = post_title.set_position(("center", 0.2), relative=True).set_duration(4.5)

    # Handles subtitles
    video = CompositeVideoClip([video, subreddit_text, post_title], size=video.size)

    clips = [video]

    for subtitle in subtitles:
        txt_clip = (TextClip(subtitle['text'],
                             fontsize=90,
                             color='white',
                             font='Tahoma-Bold',
                             stroke_color='black',
                             stroke_width=5)
                    .set_position(('center', 'center'))
                    .set_start(subtitle['start'])
                    .set_duration(subtitle['end'] - subtitle['start']))
        clips.append(txt_clip)

    final_video = CompositeVideoClip(clips)

    # Edits file name to avoid errors
    temp_title = re.sub(r'[\\/*?:"<>|]', "", title)
    if len(temp_title) > 100:
        temp_title = temp_title[:100].rsplit(' ', 1)[0]
    final_video.write_videofile(temp_title + ".mp4")


# Sets up config file
config = configparser.ConfigParser()
config.read('config.ini')

# links to reddit
reddit = praw.Reddit(
    client_id=config["Reddit"]["client_id"],
    client_secret=config["Reddit"]["client_secret"],
    user_agent=config["Reddit"]["user_agent"],
)
subreddit = reddit.subreddit(config["Reddit"]["subreddit"])

# main function call
get_posts()
