"""
Ryan Tietjen
August 2024
Contains helper functions related to obtaining the video title and body text
"""

import logging
import praw  # Reddit API; used to get posts

def get_text(config, reddit):
    """
    Determines the method to fetch posts based on the configuration settings,
    then retrieves and returns post data accordingly.

    Args:
        config (ConfigParser object): Configuration settings that dictate the method of fetching posts.
        reddit (praw.Reddit object): An authenticated Reddit instance for accessing the Reddit API.

    Returns:
        list of tuples: Each tuple contains a post's title and body text.
    """
    if config["Settings"].getboolean("use_custom_text"):
        posts_data = handle_custom_text(config)
    elif config["Settings"].getboolean("single_link"):
        posts_data = handle_single_link(config, reddit)
    else:
        posts_data = handle_multiple_posts(config, reddit)
        
    return posts_data

def handle_custom_text(config):
    """
    Fetches custom text from the configuration.

    Args:
        config (ConfigParser object): Configuration settings that include custom text details.

    Returns:
        list of tuples: Contains one tuple with the custom title and body text.
    """
    posts_data = []
    title = config["Settings"]["custom_title"]
    body = config["Settings"]["custom_body"]
    posts_data.append((title, body))
    return posts_data

def handle_single_link(config, reddit):
    """
    Retrieves a single post from Reddit using a specific URL provided in the configuration.

    Args:
        config (ConfigParser object): Configuration settings that include the URL of the post.
        reddit (praw.Reddit object): An authenticated Reddit instance for accessing the Reddit API.

    Returns:
        list of tuples: Contains one tuple with the sanitized title and body text of the post.
    """
    posts_data = []
    try:
        url = config["Settings"]["post_link"]
        post = reddit.submission(url=url)
        posts_data.append((sanitize_text(post.title), sanitize_text(post.selftext)))
    except Exception as e:
        logging.error(f"Failed to process single link: {e}")
    
    return posts_data

def handle_multiple_posts(config, reddit):
    """
    Fetches multiple posts from a specified subreddit based on configuration settings.

    Args:
        config (ConfigParser object): Configuration settings that specify the subreddit, number of posts, and time filter.
        reddit (praw.Reddit object): An authenticated Reddit instance for accessing the Reddit API.

    Returns:
        list of tuples: Contains tuples of sanitized titles and body texts from multiple posts.
    """
    posts_data = []
    try:
        subreddit = reddit.subreddit(config["Reddit"]["subreddit"])
        post_limit = int(config["Reddit"]["limit"])
        time_filter = config["Reddit"]["time_filter"]
        top_posts = subreddit.top(time_filter=time_filter, limit=post_limit)
        
        for i, post in enumerate(top_posts, start=1):
            if len(post.selftext) < 2950:
                print(f"Collecting data for {i}/{post_limit}")
                posts_data.append((sanitize_text(post.title), sanitize_text(post.selftext)))
            else:
                print(f"Post too large, skipping ({i}/{post_limit})")
    except Exception as e:
        logging.error(f"Failed to process multiple posts: {e}")
        
    return posts_data

def sanitize_text(text):
    """
    Sanitizes text by replacing specific abbreviations with their expanded forms.

    Args:
        text (str): The text to be sanitized.

    Returns:
        str: The
    """
    replacements = {
        "AITA": "A.I.T.A",
        "TIFU": "T.I.F.U",
    }
    for key, replacement in replacements.items():
        text = text.replace(key, replacement)
    return text    

