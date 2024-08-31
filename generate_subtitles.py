"""
Ryan Tietjen
August 2024
Contains helper functions related to generating the video's subtitles
"""

#--------------------------------------------------------------------------------------------------------------------
#READ THIS IF THE PROGRAM CANNOT FIND FILES
#--------------------------------------------------------------------------------------------------------------------
#ffmpeg is essential for loading the background video and audio
#Merely running "pip install ffmpeg" will not be enough for ffmpeg to be installed 
#Please follow https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ for completeness
import ffmpeg
import whisper_timestamped  # Used to generate subtitles
import os # Used for saving files to the system

def generate_subtitles(temp_audio_path):
    """
    Generates subtitles for an audio file using a pre-trained Whisper model.

    Args:
        temp_audio_path (Path object): The path to the audio file for which subtitles are to be generated.

    Returns:
        list of dicts: A list where each dictionary represents a subtitle segment containing the text, start time, and end time.

    Overview:
        This function uses the Whisper model to perform speech-to-text conversion on the audio file specified by `temp_audio_path`.
        It processes the audio file to detect spoken words and their corresponding timestamps.
        Each detected word is stored as a dictionary in the list with its text, start, and end timestamps.

    Details:
        - The function initializes the Whisper model by loading a pre-defined model configuration.
        - It then calls the transcription method to process the entire audio file.
        - For each word in the transcription result, a dictionary is created with the word's text and its start and end times.
        - These dictionaries are collected into a list which is then returned.
    """
    print("GENERATING SUBTITLES")
    subtitles = []

    model = whisper_timestamped.load_model("base")
    results = whisper_timestamped.transcribe(model, str(temp_audio_path))

    for segment in results["segments"]:
        for word in segment["words"]:
            subtitles.append({"text": word["text"],
                              "start": float(word["start"]),
                              "end": float(word["end"])})

    return subtitles
