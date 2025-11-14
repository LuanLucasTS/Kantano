from moviepy.video.io.VideoFileClip import VideoFileClip

input_video = "static/video/kda.mp4"
output_audio = "static/video/output_audio.mp3"
start_time = 30
duration = 15

video = VideoFileClip(input_video)
audio = video.audio.subclip(start_time, start_time + duration)
audio.write_audiofile(output_audio)