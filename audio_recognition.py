from audio_extract import extract_audio
from moviepy.editor import VideoFileClip
from os import listdir
import os
from audio_splitter.main import split_audio
import speech_recognition as sr
from openai import OpenAI
from pydub import AudioSegment
import math
from picklehelpers import save, load
from astrapy import DataAPIClient
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()



def extract_transcriptions():
    
    clip = VideoFileClip("./Videos/XpwUwDGo9Ds.mp4")
    swim = AudioSegment.from_mp3("./Audios/XpwUwDGo9Ds.wav")
    duration = 1000 * clip.duration 
    print( clip.duration ) # 197 seconds --> needs to be converted to ms 197 000
    split_size = 2 * 60 * 1000 + 20000 # 147000

    iterations = math.ceil(duration/split_size)
    transcripts = dict()
    j=0
    for i in range(1,iterations+1):    
       chunk = swim[j:min(i*split_size, duration)]
       chunk.export(f"./audiochunks/chunk_{i}.wav", format="wav")
       client = OpenAI()
       transcription = client.audio.transcriptions.create(
                                model="whisper-1", 
                                file=open(f"./audiochunks/chunk_{i}.wav", "rb"),
                                timestamp_granularities='segment',
                                response_format="verbose_json"
       )
       transcripts[i] = transcription
       j = split_size * i
       
    return transcripts

def create_document_format(transcipts : dict, split_time = 147):
    documents = []
    for key, value in transcipts.items():
        segments = value.model_extra.get("segments")
        for item in segments:
            id = str(item.get("id")) + "_" + str(key)
            start = item.get("start") + (key-1) * split_time # this is the first chunk of the video 0 * split time will return the original values
            end = item.get("end") + (key-1) * split_time
            text = item.get("text")
            document = dict()
            document["_id"] = id
            document["start"] = start
            document["end"] = end
            document["text"] = text
            documents.append(document)
    return documents
            
def connect_to_astra():
    client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
    database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
    collection = database.get_collection(os.environ.get("AUDIO_COLLECTION"))
    return client, database, collection



if __name__ == "__main__":   
    # Extract the audio channel from the video
    ## extract_audio(input_path="./Videos/XpwUwDGo9Ds.mp4", output_path="./Audios/XpwUwDGo9Ds.wav", overwrite=True, output_format="wav")
    if os.path.isfile("./transcripts.pickle"):
        transcripts = load("./transcripts.pickle")
    else:
        transcripts = extract_transcriptions()
        save("transcripts.pickle", transcripts)
    
    docs = create_document_format(transcripts)
    client, database, collection = connect_to_astra()
    print(transcripts.get(1).text)
    print(transcripts.get(2).text)
    for doc in docs:     
        try:
            collection.update_one(
                        {'_id': doc.get('_id')},
                {'$set': {
                '$vectorize': doc.get("text"), 
                'content': doc.get("text"), 
                'metadata': { 'ingested': datetime.now(), "start" : doc.get("start"),
                "end" : doc.get("end"),}
                }},
                upsert=True 
                    )
        except Exception as ex:
            print(ex)
            print("Retrying...")
    
   


    

    #Video needs to be chunked otherwise OpenAI throws an exception
    
    

   
    

   
    

    
  



