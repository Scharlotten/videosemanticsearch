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


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def connect_to_vectordb():
    application_end_point = os.environ.get("ASTRA_DB_API_ENDPOINT")
    application_token = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
    my_client = astrapy.DataAPIClient(application_token)
    my_database = my_client.get_database(application_end_point)
    logger.info("Successfully connected to Astra DB")    
    return my_client, my_database 


def configure_collection(database, collection=os.environ.get("COLLECTION")):
    print(database.list_collection_names())
    if collection not in database.list_collection_names():
        
        my_collection = database.create_collection(
            collection,
            dimension=512,
            #keyspace="asemjen-demo",
            metric=astrapy.constants.VectorMetric.COSINE)
        logger.info(f"Created {collection} collection")
    else:
        my_collection = database.get_collection(collection)
        logger.info("Found video collection - proceeding with the collection that exists in Astra DB")
    return my_collection


def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    logger.info(f"Found device: {device} for model projection")
    return model, preprocess, device


def load_video(path=os.environ.get("VIDEO")):
    cap = cv2.VideoCapture(path)
    logger.info("Found video and captured it")
    return cap


def load_saved_state(video_name=os.environ.get("VIDEO")):
    i = 0
    if os.path.isfile("counter.pickle"):
        state = load("counter.pickle")
        i = state.get(video_name, 0)
        if i is not None:
            i = i+1
            logger.info(f"Process is countinued from {i} as in video {video_name} found from latest state pickle file - see counter.pickle in the directory for further info")
        else:
            logger.info("Starting count from 0")
    return i

def vectorize_video(cap, model, preprocess, device, saved_progress, collection,
                       video_name=os.environ.get("VIDEO")):
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(frame_count)
    # Everything is divided by 8 because it would be too costly to calculate an embedding for every fps
    completeness = round(saved_progress/(frame_count/8))
    if round(saved_progress/(frame_count/8)) != 1:
        image_vectors = torch.zeros((round(frame_count/8), 512), device=device)
        logger.info(f"Created a list of tensors {frame_count/8}")
        cur_state = {video_name: 0}
        for j in tqdm(range(saved_progress, frame_count//8)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, j*8)   
            ret, frame = cap.read()
            with torch.no_grad():
                image_vectors[j] = model.encode_image(
                    preprocess(Image.fromarray(frame)).unsqueeze(0).to(device)
                )
                position = cap.get(cv2.CAP_PROP_POS_MSEC)
                insert_payload  = {
                    "_id" : video_name + "_" + str(j), 
                    "$vector" : image_vectors[j].tolist(), 
                    "position" : position,
                    "file" : video_name
                }
                # logger.info(f"Attempt to insert with {insert_payload=}")
                collection.insert_one(insert_payload)
                if os.path.isfile("counter.pickle"):
                    cur_state = load("counter.pickle")
                
                cur_state[video_name] = j

                save("counter.pickle", cur_state)
    else:
        logger.info(f"State is {completeness*100}% completed")
    return

def get_most_similar_frame(query: str, model, device, my_collection, video_name=os.environ.get("VIDEO")):
    query_vector = model.encode_text(clip.tokenize([query]).to(device))
    example = query_vector.tolist()[0]
    result = my_collection.find_one({"file": video_name}, vector=example, include_similarity=True)
    print(example)
   
    return result.get("position"), result.get("$similarity")

from math import floor
if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path, override=True)
    video_path = os.environ.get("VIDEO")
    #video_path = "swimming.mp4"
    logger.info(f"This is the video {video_path}")
    my_client, my_database = connect_to_vectordb() 
    my_collection = configure_collection(my_database)
    model, prepocess, device = load_model()
    cap = load_video(video_path)
    i = load_saved_state(video_path)
    a = vectorize_video(cap, model, prepocess, device, i, my_collection, video_name=video_path)
    position, similarity = get_most_similar_frame("Swimmers stop swimming - race is over", model, device, my_collection, video_path)
    #position = get_most_similar_frame("Crowd cheering happily.", model, device, my_collection, video_name=video_path)
    minutes = position // 1000 // 60
    seconds = (position // 1000) % 60
    logger.info(f"Position {minutes} minutes and {seconds} seconds ")
    #ffmpeg_extract_subclip(video_path, position*0.001-4, position*0.001+15, targetname="interest_2.mp4")
    #The moment swimmers reach the end of the pool and the final score is displayed race stops
    #swimmers before jumping into the pool
    # swimmer wins