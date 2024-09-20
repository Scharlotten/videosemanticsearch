from pytubefix import YouTube
import os
import re
from pytubefix.cli import on_progress


url_input = "https://www.youtube.com/watch?v=XpwUwDGo9Ds"




yt =  YouTube(url_input)
s = yt.title
# s = re.sub("[a-zA-z]*\\|", "", s)
filename = yt.video_id + ".mp4"
yt.streams.get_highest_resolution().download(os.path.join(os.path.curdir,"Videos"), filename)
#logger.info(f"Successfully donwloaded file {filename}")