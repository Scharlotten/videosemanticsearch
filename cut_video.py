from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

found_value = 293760.0
ffmpeg_extract_subclip("swimming.mp4", found_value*0.001-3, found_value*0.001+15, targetname="test.mp4")