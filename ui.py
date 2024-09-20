import streamlit as st
from io import StringIO
from datetime import datetime
import logging
import astrapy.database
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from tqdm import tqdm
import astrapy
import os 
from dotenv import load_dotenv
from picklehelpers import save, load
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from math import floor 
from pytubefix import YouTube
from modulized import load_model, get_most_similar_frame, load_video, load_saved_state, vectorize_video, connect_to_vectordb, configure_collection
import re
from call_langflow import call_langflow
from datetime import timedelta

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

st.title("Search Videos - by text")
#st.image("paris_olympics.jpg", width=200)


sport_list = ["Swimming", "Other"]
tab1, tab2 = st.tabs(sport_list)

@st.cache_resource
def get_db_conn():
    my_client, my_database = connect_to_vectordb() 
    return my_client, my_database

@st.cache_data
def load_ai_model():
    model, prepocess, device = load_model()
    return model, prepocess, device

with tab1:
   st.header(sport_list[0])
   cur = st.video("Videos/XpwUwDGo9Ds.mp4")
   text_input = st.text_input( "What do you enjoy watching?", key="Pre-defined")
   text_input2 = st.text_input("How would you search the audio stream?", key="Pre-defined2")
   if text_input:
        my_client, my_database = connect_to_vectordb() 
        my_collection = configure_collection(my_database)
        model, prepocess, device = load_model()
        position, similarity = get_most_similar_frame(text_input, model, device, my_collection)
        logger.info(f"Position {floor(position*0.001/60)}")
        cur.empty()
        st.video("Videos/XpwUwDGo9Ds.mp4", start_time=position*0.001)  #first second and third places are displayed in the swim lanes on the pool 
        #1 2 and 3rd  places are displayed in the swim lanes on the pool race stops
        st.text(similarity)
        # Do the same for the audio part
   
   if text_input2:
        time, sentence = call_langflow(text_input2)
        st.text(f"Audio data {sentence} at {str(timedelta(seconds=time))}")
        st.video("Videos/XpwUwDGo9Ds.mp4", start_time=time)

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
        # s = yt.title
        # s = re.sub("[a-zA-z]*\\|", "", s)
        filename = yt.video_id + ".mp4"
        yt.streams.first().download(path, filename)
        logger.info(f"Successfully donwloaded file {filename}")
        
        
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        filename = uploaded_file.name
        # To read file as bytes:
        with open(os.path.join(path, filename), "wb") as binary_file:
        # Write bytes to file
            binary_file.write(bytes_data)
        vid = st.video(bytes_data)    

    if (url_input or uploaded_file) and text_input:
        my_client, my_database = get_db_conn()
        my_collection = configure_collection(my_database)
        model, prepocess, device = load_ai_model()
        full_path = os.path.join(path, filename)
        cap = load_video(full_path)
        logger.info(f"{cap.get(cv2.CAP_PROP_POS_MSEC)} is the number of frames")
        i = load_saved_state(filename)
        a = vectorize_video(cap, model, prepocess, device, i, my_collection, filename)

        position, similarity = get_most_similar_frame(text_input, model, device, my_collection, filename)
        logger.info(f"Position {int(position/1000)//60}:{int(position/1000) %60}")
        st.write(f"Video position is: {position}")

        vid.empty()
        st.video(url_input or uploaded_file, start_time=position*0.001-3)

   



