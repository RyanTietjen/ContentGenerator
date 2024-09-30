# ContentGenerator
Short-Form Content Generator for TikTok, Youtube Shorts, etc.  
Created by Ryan Tietjen.  
January 2024.

[Sample 1](https://www.tiktok.com/@the.reddit.awards/video/7402646530714389790)\
[Sample 2](https://www.tiktok.com/@the.reddit.awards/video/7403080230232919326)\
[Sample 3](https://www.tiktok.com/@the.reddit.awards/video/7403470834024615214)

[Old Sample 1](https://youtu.be/CfCJ2r-iS5U)  
[Old Sample 2](https://youtu.be/kbGNfAiELp0)  
[Old Sample 3](https://youtu.be/6RRYg48KFPU)  

HOW TO USE:

1. Download main.py and config.ini, and move files into a python project.  
2. Setup background video.  
   -Obtain a 16x9 aspect ratio background video and name it "background.mp4."  
   -In your python project, move background.mp4 to the same file location as main.py.  
   -The video used in the samples can be found [here](https://www.youtube.com/watch?v=952ILTHDgC4).  
   -RECOMMENDED: Use [stacher.io](https://stacher.io/) to download the video from youtube (free).  
   -RECOMMENDED: Use [ClipChamp](https://clipchamp.com/en/) to reformat the video to 16x9.  
3. Install Dependencies  
   -Use "pip install \[dependency\]"  
   -OR (in pycharm) go to File -> Settings -> Project: \[Project Name\] -> Python Interpreter -> click the "+" -> search for dependencies -> Install Package  
   -In addition, [ImageMagick](https://imagemagick.org/) must be installed.  
4. Obtain Reddit client_id, client_secret, user_agent (fill in this information in the config file)  
   -REQUIRED: Create a new app [here](https://www.reddit.com/prefs/apps)
5. Obtain AWS access_key_id and secret_access_key (fill in this information in the config file)  
   -Information can be found [here](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/home)
