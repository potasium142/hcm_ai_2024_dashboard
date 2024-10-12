import requests
import json

ENDPOINT = "http://0.0.0.0:11434/api/chat"

MSG_TEMPLATE = {
    "model": "llama2",
    "messages": [{
        "role": "user",
        "content": ""
    }],
    "stream": True
}


def sent_chat(msg):
    msg_dict = MSG_TEMPLATE.copy()
    msg_dict["messages"][0]["content"] = msg
    r = requests.post(
        ENDPOINT,
        json=msg_dict,
        stream=True
    )
    for msg in r.iter_lines():
        if msg:
            yield json.loads(msg)


for i in sent_chat("why the game amogus become popular"):
    print(i)
