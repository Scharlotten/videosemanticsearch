**Video Semantic Search**

How to use:
Make a copy of the .env_template file and rename it .env 

Fill out the variables:
Make sure you have an AstraDB account a token and and API key

Create the collections to store the vectorized data in in AstraDB 
My collection names were 1. swimming and 2. audio

Install Python - I used 3.12.3 at the time of creation

pip install requirements.txt

To run the programme run - streamlit run ui.py
