import streamlit as st
from io import StringIO
from datetime import datetime
import astrapy
import logging
import astrapy.database
import clip
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import torch
from PIL import Image
from tqdm import tqdm
import astrapy
import os 
from dotenv import load_dotenv
from picklehelpers import save, load
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from math import floor 
from pytube import YouTube
from modulized import load_model, get_most_similar_frame, load_video, load_saved_state, vectorize_video, connect_to_vectordb, configure_collection

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

st.title("Welcome to the Olympics 2024")
st.image("paris_olympics.jpg", width=200)


sport_list = ["Swimming", "Other"]
tab1, tab2 = st.tabs(sport_list)


with tab1:
   st.header(sport_list[0])
   cur = st.video("swimming.mp4")
   text_input = st.text_input( "What do you enjoy watching?", key="Pre-defined")
   if text_input:
        my_client, my_database = connect_to_vectordb() 
        my_collection = configure_collection(my_database)
        model, prepocess, device = load_model()
        position = get_most_similar_frame(text_input, model, device, my_collection)
        logger.info(f"Position {floor(position*0.001/60)}")
        cur.empty()
        st.video("swimming.mp4", start_time=position*0.001)  

with tab2:
    st.header(sport_list[1])
    uploaded_file = st.file_uploader("Choose a file")
    url_input = st.text_input("Or paste video URL here", key="youtube")
    text_input = st.text_input("What do you enjoy watching?")

    path = os.path.join(os.path.dirname(__file__), 'Videos')
    filename = datetime.now().strftime("%Y%m%d_%H%M%S.mp4")

    if url_input:
        vid = st.video(url_input)
        yt =  YouTube(url_input)
        filename = yt.title
        yt.streams.first().download(path, filename)
        
        
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        filename = uploaded_file.name
        # To read file as bytes:
        with open(os.path.join(path, filename), "wb") as binary_file:
        # Write bytes to file
            binary_file.write(bytes_data)
        vid = st.video(bytes_data)    

    if (url_input or uploaded_file) and text_input:
        my_client, my_database = connect_to_vectordb() 
        my_collection = configure_collection(my_database)
        model, prepocess, device = load_model()
        full_path = os.path.join(path, filename)
        cap = load_video(full_path)
        logger.info(f"{cap.get(cv2.CAP_PROP_POS_MSEC)} is the number of frames")
        i = load_saved_state(filename)
        a = vectorize_video(cap, model, prepocess, device, i, my_collection, filename)
        position = get_most_similar_frame(text_input, model, device, my_collection, filename)
        logger.info(f"Position {int(position/1000)//60}:{int(position/1000) %60}")
        vid.empty()
        st.video(url_input or uploaded_file, start_time=position*0.001-3)

   

# with st.sidebar:
#     genre = st.radio(
#     "What do you enjoy watching?",
#     [":swimmer: Swimming", ":soccer: Football", ":rowboat: kayak", ":horse_racing: Showjump", ":rainbow[Other]"],
#     #captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
#     )
#     if genre == ":rainbow[Other]":
#         pass
        
#     else:
#         st.write("You didn't select comedy.")



