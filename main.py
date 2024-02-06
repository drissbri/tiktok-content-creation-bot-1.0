from moviepy.editor import VideoFileClip, VideoClip, AudioFileClip, concatenate_videoclips,CompositeAudioClip
import os
import random
import numpy as np
from Naked.toolshed.shell import execute_js

# Function to load all videos in the given directory
def load_videos_in_directory(directory_path):
    paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.mp4')]
    return paths

def load_audios_in_directory(directory_path):
    paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.mp3')]
    return paths

# Function to pick a random video from a list
def pick_random_video(videos_list):
    return random.choice(videos_list)

def lighten_blend(frame1, frame2):
    # Convert frames to numpy arrays for pixel-wise blending
    np_frame1 = np.array(frame1)
    np_frame2 = np.array(frame2)
    
    # Apply the "lighten" blend mode
    blended_frame = np.maximum(np_frame1, np_frame2)
    
    return blended_frame

def screen_blend(frame1, frame2):
    # Convert frames to numpy arrays for pixel-wise blending
    np_frame1 = np.array(frame1) / 255.0
    np_frame2 = np.array(frame2) / 255.0
    
    # Apply the "screen" blend mode
    inverted_result = 1.0 - (1.0 - np_frame1) * (1.0 - np_frame2)
    blended_frame = (inverted_result * 255).astype(np.uint8)
    
    return blended_frame

# Load all background and content videos
background_videos = load_videos_in_directory('background_content')
background_hooks = load_videos_in_directory('background_hook')
content_videos = load_videos_in_directory('content') 
hook_videos = load_videos_in_directory('hook') 
background_musics = load_audios_in_directory('music') 

# Pick random content video and import it
content_video_path = pick_random_video(content_videos)
content_video = VideoFileClip(content_video_path, has_mask=True)

# Pick random background video and import it
background_video_path = pick_random_video(background_videos)
background_video = VideoFileClip(background_video_path)

# Pick random hook video and import it
hook_video_path = pick_random_video(hook_videos)
hook_video = VideoFileClip(hook_video_path)

# Pick random background video and import it
background_hook_path = pick_random_video(background_hooks)
background_hook = VideoFileClip(background_hook_path)

# Pick random background music and import it
background_music_path = pick_random_video(background_musics)
background_music = AudioFileClip(background_music_path)


#                            MAKING CONTENT VIDEO                          #

# Get the duration of the background video
background_video_duration = background_video.duration

# Set the desired duration for the random portion (in seconds)
random_portion_duration = content_video.duration

# Calculate a random start time for the subclip
random_start_time = random.uniform(0, background_video_duration - random_portion_duration)

# Create a subclip with the random portion
background_video_final = background_video.subclip(random_start_time, random_start_time + random_portion_duration)

# Ensure both clips have the same duration and size
background_video_final = background_video_final.resize(content_video.size)  # Resize background_video_final to match content_video's size

# Process each frame and create a new VideoClip
blended_frames = [lighten_blend(frame1, frame2) for frame1, frame2 in zip(content_video.iter_frames(), background_video_final.iter_frames())]
blended_content = VideoClip(lambda t: blended_frames[int(t * content_video.fps)], duration=content_video.duration)


# Ensure the audio clip matches the video clip's duration
background_music = background_music.subclip(0, content_video.duration)

# Adjust the volume of the audio by a factor (0.5 reduces volume to half, 2 doubles it)
background_music = background_music.volumex(0.1)

blended_content_audio = CompositeAudioClip([content_video.audio, background_music])

# Set the audio of the video clip to the background music
blended_content_with_music = blended_content.set_audio(blended_content_audio)


#                            MAKING CONTENT HOOK                           #

# Ensure both clips have the same duration and size
background_hook_final = background_hook.subclip(0, hook_video.duration)

# Resize background_hook_final to match hook_video's size
background_hook_final = background_hook_final.resize(hook_video.size) 
# Process each frame and create a new VideoClip
blended_frames1 = [lighten_blend(frame3, frame4) for frame3, frame4 in zip(hook_video.iter_frames(), background_hook_final.iter_frames())]
blended_hook = VideoClip(lambda f: blended_frames1[int(f * hook_video.fps)], duration=hook_video.duration)

#  audio from clip
blended_hook = blended_hook.set_audio(hook_video.audio)


# Concatenate the clips in the desired order
concatenated_clip = concatenate_videoclips([blended_hook, blended_content_with_music])
concatenated_clip = concatenated_clip.volumex(1.5)


# Write the blended video to a file
concatenated_clip.write_videofile("output.mp4", fps=24)


#                       METADATA

# Description & Tags

# Making title list
with open('metadata/title.txt', 'r') as f:
    # Read the contents of the file
    contents = f.read()
    # Split the contents into a list of words
    title_list = contents.split(',')
    # Remove any leading or trailing white space from each word
    title_list = [word.strip() for word in title_list]

# Making Description list
with open('metadata/description.txt', 'r') as f:
    # Read the contents of the file
    contents = f.read()
    # Split the contents into a list of words
    description_list = contents.split(',')
    # Remove any leading or trailing white space from each word
    description_list = [word.strip() for word in description_list]

# Making tags list
with open('metadata/tags.txt', 'r') as f:
    # Read the contents of the file
    contents = f.read()
    # Split the contents into a list of words
    tag_list = contents.split(',')
    # Remove any leading or trailing white space from each word
    tag_list = [word.strip() for word in tag_list]


# Constructing Title
title = f"{random.choice(title_list)} #dogs #pets\n"  

# Constructing Description
description = f"""{random.choice(description_list)} {random.choice(description_list)} 2023 | SUBSCRIBE FOR MORE
#{random.choice(tag_list)} #{random.choice(tag_list)} #{random.choice(tag_list)} #{random.choice(tag_list)} #viral #shorts
"""

# Construct the video tags
tags = random.choice(tag_list)+','+random.choice(tag_list)+','+random.choice(tag_list)+','+random.choice(tag_list)+','+random.choice(tag_list)

with open("video_text.txt", 'w') as file:
    file.write(title+description+tags)


#Finishing
print("Video Finished Successfully!")