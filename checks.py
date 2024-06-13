import clip
import logging
import cv2
import matplotlib.pyplot as plt
#import torch 
from PIL import Image

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

#device = "cuda" if torch.cuda.is_available() else "cpu"
#model, preprocess = clip.load("ViT-B/32", device=device)

video_path = "swimming.mp4"
cap = cv2.VideoCapture(video_path)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


cap.set(cv2.CAP_PROP_POS_FRAMES, 8856)
ret, frame = cap.read()
plt.imshow(Image.fromarray(frame))
plt.show()