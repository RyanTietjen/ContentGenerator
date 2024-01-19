# ContentGenerator
Short-Form Content Generator for Tiktok, Youtube Shorts, etc.  
Created by Ryan Tietjen.  
January 2024.

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
   -In addition, [ImageMagick](https://imagemagick.org/) must be installed,
4. Obtain Reddit client_id, client_secret, user_agent (fill in this information in the config file)  
   -REQUIRED: Create a new app [here](https://www.reddit.com/prefs/apps)
5. Obtain AWS access_key_id and secret_access_key (fill in this information in the config file)
