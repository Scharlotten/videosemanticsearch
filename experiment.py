
import logging
import cv2
import os 
from math import floor 
from pytube import YouTube
from modulized import get_most_similar_frame, load_video, load_saved_state, vectorize_video, connect_to_vectordb, configure_collection, load_model


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    url_input = "https://www.youtube.com/watch?v=V79iAlOveqI"
    text_input = "goal"
    yt = YouTube(url_input)
   
    path = os.path.join(os.path.dirname(__file__), 'Videos')
    YouTube(url_input).streams.first().download(path)
    
    client, database = connect_to_vectordb()
    collection = configure_collection(database)
    model, prepocess, device = load_model()
    cap = load_video(os.path.join(path, yt.title))
    logger.info(f"{cap.get(cv2.CAP_PROP_FRAME_COUNT)} is the number of frames")
    i = load_saved_state(yt.title)
    a = vectorize_video(cap, model, prepocess, device, i, collection, yt.title)
    position = get_most_similar_frame(text_input, model, device, collection, yt.tile)
    logger.info(f"Position {floor(position*0.001/60)}")

if __name__ == "__main__":
    main()