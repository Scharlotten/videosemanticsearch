from pathlib import Path
import logging
import astrapy.database
import clip
import cv2
import torch
from PIL import Image
from tqdm import tqdm
import astrapy
import os 
from picklehelpers import save, load



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ASTRA_DB_APPLICATION_TOKEN = "AstraCS:jppFoZXHRrdzefOfmwNUiJQy:b7b59e9e2abd8a72bc29326856a2f6f7c8828bc811968f23a8911b3d44eb9dfd"
ASTRA_DB_API_ENDPOINT = "https://fa93326d-dfb1-403e-a0ce-da43f6756bb3-us-east-2.apps.astra.datastax.com"

my_client = astrapy.DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
my_database = my_client.get_database(ASTRA_DB_API_ENDPOINT)
logger.info("Successfully connected to Astra DB")    

if "video" not in my_database.list_collection_names():
    my_collection = my_database.create_collection(
        "video",
        dimension=512,
        metric=astrapy.constants.VectorMetric.COSINE)
    logger.info("Created video collection")

else:
    my_collection = my_database.get_collection("video")
    logger.info("Found video collection - proceeding with the collection that exists in Astra DB")


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
logger.info(f"Found device: {device} for model projection")

video_path = "swimming.mp4"
cap = cv2.VideoCapture(video_path)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Pickle functionality is added so if the code fails the whole video doesn't need to be pared again
if os.path.isfile("counter.pickle"):
        i = load("counter.pickle")+1
        cap.set(cv2.CAP_PROP_POS_FRAMES, i) # continue the video from the latest recorded frame 
        logger.info(f"Process is countinued from {i} as found from latest state pickle file - see counter.pickle in the directory for further info")
else:
     i = 0
     logger.info("Starting count from 0")

image_vectors = torch.zeros((round(frame_count/8), 512), device=device)
logger.info(f"Created a list of tensors {frame_count/8}")

for j in tqdm(range(i, round(frame_count/8))):
    cap.set(cv2.CAP_PROP_POS_FRAMES, j*8)   
    ret, frame = cap.read()
    with torch.no_grad():
        image_vectors[j] = model.encode_image(
            preprocess(Image.fromarray(frame)).unsqueeze(0).to(device)
        )
        #print(len(image_vectors[j].tolist()))
        position = cap.get(cv2.CAP_PROP_POS_MSEC)
        my_collection.insert_one({"_id" : video_path + "_" + str(j), "$vector" : image_vectors[j].tolist(), "position" : position})
        save("counter.pickle", j)



def get_most_similar_frame(query: str) -> tuple[int, list[float]]:
    query_vector = model.encode_text(clip.tokenize([query]).to(device))
    return query_vector



query= "The moment swimmers reach the end of the pool and the final score is displayed"

test = get_most_similar_frame(query)
example = test[0]
result = my_collection.find_one({}, vector=example)

print(example.tolist())
print(result)
