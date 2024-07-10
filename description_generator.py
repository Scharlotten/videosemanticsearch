import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv
from picklehelpers import save

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY")))

video = cv2.VideoCapture("Videos/swimming.mp4")

frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

base64Frames = []
for i in range(0, frame_count, 24):
    video.set(cv2.CAP_PROP_POS_FRAMES, i) 
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
video.release()
print(len(base64Frames), "frames read.")



PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames from a video that I want to upload. \
              Generate a compelling description that I can upload along with the video with tags.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
        ],
    },
]
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}
result = client.chat.completions.create(**params)
save("openai_result.pickly", result)

print(result)