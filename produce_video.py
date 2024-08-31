"""
Ryan Tietjen
August 2024
Contains helper functions related to producing the final video.

This module includes utilities for generating video clips, wrapping text, selecting thumbnails based on text lines, and assembling all components into a final video file. 
It leverages the `moviepy.editor` library extensively along with some additional Python libraries for file and text manipulation.
"""


from moviepy.editor import *  # Produces the final video
import random  # used to get a random point from the background video
import re # Used to edit file text
from pathlib import Path # Used for storing/loading assets and final videos

def generate_random_clip_timestamps(duration, audio_duration):
    """
    Generates start and end timestamps for a video clip based on the provided duration constraints.

    Args:
        duration (int): The total duration of the background video in seconds.
        audio_duration (int): The desired duration of the audio clip in seconds.

    Returns:
        tuple: A tuple containing the start and end timestamps for the clip.
    """
    max_start = int(duration - audio_duration)  # Maximum start point for the clip
    start_time = int(random.randint(0, max_start))  # Randomly select a start time
    end_time = int(start_time + audio_duration + 1)  # Calculate end time based on audio duration
    return start_time, end_time


def wrap_text(text, font, max_width):
    """
    Wraps text into multiple lines so that each line does not exceed a specified pixel width.

    Args:
        text (str): The text to be wrapped.
        font (str): The font used for rendering the text.
        max_width (int): The maximum width in pixels of the text line.

    Returns:
        tuple: A tuple containing the wrapped text and the number of lines.
    """
    words = text.split()
    lines = []
    line = []

    # Create a TextClip for measuring text width
    for word in words:
        # Check the width of the line with the new word added
        line_plus_word = ' '.join(line + [word])
        text_clip = TextClip(line_plus_word, font=font, fontsize=60)
        text_width, _ = text_clip.size

        # If the line is too wide, start a new line
        if text_width > max_width:
            lines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)

    # Add the last line
    lines.append(' '.join(line))
    return '\n'.join(lines), len(lines)

def set_thumbnail_image_path(num_lines, assets_path):
    """
    Selects the appropriate thumbnail image path based on the number of text lines.

    Args:
        num_lines (int): The number of lines in the title or text.
        assets_path (Path): The file path to the directory containing thumbnail templates.

    Returns:
        Path: The path to the selected thumbnail image file.
    """
    if num_lines == 1:
        thumbnail_image_path = assets_path / "Template_1.png"
    elif num_lines == 2:
        thumbnail_image_path = assets_path / "Template_1.png"
    elif num_lines == 3:
        thumbnail_image_path = assets_path / "Template_2.png"
    elif num_lines == 4:
        thumbnail_image_path = assets_path / "Template_3.png"
    elif num_lines == 5:
        thumbnail_image_path = assets_path / "Template_4.png"
    elif num_lines == 6:
        thumbnail_image_path = assets_path / "Template_5.png"
    else:
        thumbnail_image_path = assets_path / "Template_6.png"
    return thumbnail_image_path

def produce_final_video(title, subtitles, temp_audio_path, background_video_path, assets_path, config):
    """
    Combines audio, subtitles, and video clips to produce the final video.

    Args:
        title (str): The title of the video.
        subtitles (list of dicts): A list of subtitle dictionaries with 'text', 'start', and 'end' keys.
        temp_audio_path (Path): The path to the temporary audio file.
        background_video_path (Path): The path to the background video file.
        assets_path (Path): The path to the directory containing assets like thumbnail templates.

    Produces a video file combining all elements and handles layout of text and subtitle overlays.
    """
    print("GENERATING VIDEO")
    
    #Make sure a "?" is at the end of the title if appropriate
    if config["Settings"].getboolean("force_question_mark"):
        if title.endswith('.'):
            title = title[:-1] + '?'
        elif not re.match(r'.*[^\w\s]$', title):
            title += '?'
        
    tts = AudioFileClip(str(temp_audio_path))
    new_tts = CompositeAudioClip([tts])

    video = VideoFileClip(str(background_video_path))

    start, end = generate_random_clip_timestamps(video.duration, tts.duration)

    video = video.subclip(start, end)
    video.audio = new_tts

    # Produces the title text seen in the thumbnail.
    wrapped_title, num_lines = wrap_text(title, "Reddit", max_width=1100)

    if config["Settings"].getboolean("use_custom_thumbnail_images"):
        color = 'black'
        stroke_color = 'black'
        stroke_width = 2.3
        interline = -7
        fontsize = 45
        thumbnail_image_path = set_thumbnail_image_path(num_lines, assets_path)

        thumbnail_image = ImageClip(str(thumbnail_image_path)).set_duration(6).set_position(('center', 320)).crossfadeout(1)
        position = (140, 485)
        relative = False
    else:
        color = 'white'
        stroke_color = 'white'
        stroke_width = 6
        fontsize = 80
        interline = -22
        position = ("center", 0.25)
        relative = True

    post_title = TextClip(wrapped_title,
                          fontsize=fontsize,
                          color=color,
                          font='Reddit',
                          align="West",
                          stroke_color=stroke_color,
                          interline=interline,
                          stroke_width=stroke_width)
    


    post_title = post_title.set_position(position, relative=relative).set_duration(6).crossfadeout(1)


    

    # Handles subtitles
    if config["Settings"].getboolean("use_custom_thumbnail_images"):
        video = CompositeVideoClip([video, thumbnail_image, post_title], size=video.size)
    else:
        video = CompositeVideoClip([video, post_title], size=video.size)

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
    
    # title = results_path / temp_title
    title = Path("D:\\tiktok") / temp_title
    final_video.write_videofile(str(title) + ".mp4")
