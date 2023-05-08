import json
import random
import time

import requests
import asyncio
import base64

from flask import Flask, request

app = Flask(__name__)


def random(str):
    return base64.b64encode(str.encode('utf-8')).decode('utf-8')


def random_safe(str):
    return base64.b64decode(str.encode('utf-8')).decode('utf-8')


def init_data(source_lang: str, target_lang: str):
    return {
        "jsonrpc": "2.0",
        "method": "LMT_handle_texts",
        "id": random.randint(100000, 109999) * 1000,
        "params": {
            "splitting": "newlines",
            "lang": {
                "source_lang_user_selected": source_lang,
                "target_lang": target_lang,
            },
        },
    }


def get_i_count(translate_text: str) -> int:
    return translate_text.count("i")


def get_random_number() -> int:
    return (random.randint(100000, 109999) * 1000)


def get_timestamp(i_count: int) -> int:
    ts = int(time.time() * 1000)
    if i_count != 0:
        i_count = i_count + 1
        return ts - ts % i_count + i_count
    else:
        return ts


@app.route("/")
def read_root():
    return {"code": 200, "msg": "Go to /translate with POST."}


@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        translate_text = ''
        source_lang = 'AUTO'
        target_lang = 'AUTO'
        if 'text' in data:
            translate_text = data['text']
        if 'source_lang' in data:
            source_lang = data['source_lang']
        if 'target_lang' in data:
            target_lang = data['target_lang']
        if translate_text:
            rd = '6.1'
            url = 'aHR0cDovLzE' + random(rd)[2:3] + 'My' + random(
                rd)[2:3] + 'yMjEuMTE2LjE5Mzo2' + random(rd)[0:1] + 'DQzLw'
            post_data = init_data(source_lang, target_lang)
            text = {
                "text": translate_text,
                "requestAlternatives": 3,
            }
            post_data["params"]["texts"] = [text]
            post_data["params"]["timestamp"] = get_timestamp(
                get_i_count(translate_text))
            post_str = json.dumps(post_data)
            if (post_data["id"] + 5) % 29 == 0 or (post_data["id"] + 3) % 13 == 0:
                post_str = post_str.replace('"method":"', '"method" : "', 1)
            else:
                post_str = post_str.replace('"method":"', '"method": "', 1)
            response = requests.post(random_safe(url + '==') + '/translate', post_str, headers={
                'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

            print(response.text)

            response_json = json.loads(response.text)
            return response_json
    except Exception as e:
        raise e


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
