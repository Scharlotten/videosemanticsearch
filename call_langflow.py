import requests
import json 
from dotenv import load_dotenv
import os 


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path) 


def call_langflow(message_input:str):
        
    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'Authorization': os.environ["LANGFLOW_AUTOHORIZATION"],
    }

    params = {
        'stream': 'false',
    }

    json_data = {
        'input_value': message_input,
        'output_type': 'chat',
        'input_type': 'chat',
    }

    response = requests.post('https://api.langflow.astra.datastax.com/lf/f2fa8022-32cc-4137-8887-358cb1476ea6/api/v1/run/a7dfb0ef-11be-402e-8f5d-0f0536547b69', params=params, headers=headers, json=json_data)

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '{"input_value": "Quote at least one sentence which is closest to indicating that the race is over", "output_type": "chat", "input_type": "chat"}'
    #response = requests.post('https://api.langflow.astra.datastax.com/lf/f2fa8022-32cc-4137-8887-358cb1476ea6/api/v1/run/a7dfb0ef-11be-402e-8f5d-0f0536547b69', params=params, headers=headers, data=data)
    temp = response.json()
    try:
        s = temp.get("outputs")[0].get("outputs")[0].get("results").get("message").get("data").get("text").strip('` \n')
        output_dict = json.loads(s[4:])
        time = output_dict.get("Time")
        sentence = output_dict.get("Answer")
    except Exception as e:
        print(f"Failed to query data {e}")

    print(time)
    print(sentence)
    return time, sentence

