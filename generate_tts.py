"""
Ryan Tietjen
August 2024
Contains helper functions related to generating TTS
"""

#--------------------------------------------------------------------------------------------------------------------
#READ THIS IF THE PROGRAM CANNOT FIND FILES
#--------------------------------------------------------------------------------------------------------------------
#ffmpeg is essential for loading the background video and audio
#Merely running "pip install ffmpeg" will not be enough for ffmpeg to be installed 
#Please follow https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ for completeness
import ffmpeg
from boto3 import Session  # AWS Polly client; used for TTS


# Produces tts
def text_to_speech(text,
                   config,
                   temp_audio_path,
                   output_format='mp3', 
                   voice_id='Matthew', 
                   region_name = 'us-east-1'):
    """
    Converts text to speech using AWS Polly, saves the audio stream to a specified path.

    Args:
        text (str): The text string to be converted into speech.
        config (dict): A dictionary containing AWS credentials (`aws_access_key_id` and `aws_secret_access_key`).
        temp_audio_path (Path object): The path where the audio file will be saved. This should be a Path object that supports methods like `open` and `mkdir`.
        output_format (str, optional): The format of the output audio file. Defaults to 'mp3'.
        voice_id (str, optional): The identifier for the voice to use in text-to-speech conversion. Defaults to 'Matthew'.
        region_name (str, optional): The AWS region where the Polly client will be initialized. Defaults to 'us-east-1'.

    This function initializes an AWS Polly client with given AWS credentials and the specified region.
    It then requests the AWS Polly service to synthesize speech from the provided text, using the specified voice and format.
    The resulting audio stream is written to the file path specified by `temp_audio_path`.
    """
    print("GENERATING TTS")
    session = Session(aws_access_key_id=config["AWS"]["aws_access_key_id"],
                      aws_secret_access_key=config["AWS"]["aws_secret_access_key"],
                      region_name=region_name).client("polly")


    response = session.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    # Save audio to a file
    temp_audio_path.parent.mkdir(parents=True, exist_ok=True)
    with temp_audio_path.open('wb') as file:
        file.write(response['AudioStream'].read())
