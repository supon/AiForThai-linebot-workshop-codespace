import json

# For Partii STT
import re

# For Vaja9
import wave

import requests
from aift import setting

# AIForThai import
from aift.nlp import (
    g2p,  # 2. G2P
    ner,  # 1.1 TNER
    sentiment,  # 8. Sentiment analysis
    similarity,  # 4. Word similarity
    soundex,  # 3. Soundex
    tag,  # 6. Tag Suggestion
    text_cleansing,  # 5. Text cleasing
    tokenizer,  # 1. Tokenizer
)
from aift.nlp.alignment import (
    en_alignment,  # 9.1. English-Thai Word Aligner
    zh_alignment,  # 9.2. Chinese-Thai Word Aligner
)
from aift.nlp.longan import sentence_tokenizer, tagger, token_tagger  # 1.2. Longan
from aift.nlp.longan import tokenizer as logan_tokenizer
from aift.nlp.translation import (
    en2th,  # 7.3. English to Thai
    th2en,  # 7.4. Thai to English
    th2zh,  # 7.2. Thai to Chinese
    zh2th,  # 7.1. Chinese to Thai
)
from aift.speech import tts
from fastapi import APIRouter, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    AudioMessage,
    AudioSendMessage,
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from app.configs import Configs

router = APIRouter(tags=["NLP"], prefix="/nlp")

cfg = Configs()

setting.set_api_key(cfg.AIFORTHAI_APIKEY)  # AIFORTHAI_APIKEY
line_bot_api = LineBotApi(cfg.LINE_CHANNEL_ACCESS_TOKEN)  # CHANNEL_ACCESS_TOKEN
handler = WebhookHandler(cfg.LINE_CHANNEL_SECRET)  # CHANNEL_SECRET


@router.post("")
async def nlp_demo(request: Request):
    """
    Line Webhook endpoint สำหรับรับข้อความจาก Line Messaging API และประมวลผลข้อความด้วย AI FOR THAI

    ฟังก์ชันนี้ทำหน้าที่:
    1. รับ HTTP POST Request จาก Line Webhook
    2. ตรวจสอบลายเซ็น (X-Line-Signature) เพื่อยืนยันความถูกต้องของข้อความ
    3. ส่งข้อความไปยัง handler เพื่อประมวลผลอีเวนต์ที่ได้รับ
    4. รองรับการประมวลผลข้อความ (TextMessage) และเสียง (AudioMessage):
        - สำหรับข้อความ (TextMessage): ตรวจจับคำสั่ง NLP และเรียกใช้ฟังก์ชันที่เกี่ยวข้อง เช่น Tokenizer, Translation, Sentiment Analysis เป็นต้น
        - สำหรับเสียง (AudioMessage): แปลงเสียงเป็นข้อความด้วย AI FOR THAI Speech-to-Text (Partii) และส่งข้อความตอบกลับไปยังผู้ใช้
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode("UTF-8"), signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token or channel secret.")
    return "OK"


@handler.add(MessageEvent, message=AudioMessage)
def handle_voice_message(event):
    # #14. SPEECH TO TEXT (Partii)
    # Get the audio file from LINE
    message_content = line_bot_api.get_message_content(event.message.id)

    # Save the audio content to a file (optional, for further processing)
    with open("received_audio.wav", "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    # Call ParTii function
    text = callPartii("received_audio.wav")

    # Call partii4 or partii5 in Python package
    # text = partii4.transcribe("received_audio.wav", return_json=True)
    # text = result['message']
    send_message(event, str(text))


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_input = event.message.text.strip()
    command_list = [
        "#trexplus",
        "#lexto",
        "#trex++",
        "#tner",
        "#g2p",
        "#soundex",
        "#thaiwordsim",
        "#wordapprox",
        "#textclean",
        "#tagsuggest",
        "#mtch2th",
        "#mtth2ch",
        "#mten2th",
        "#mtth2en",
        "#ssense",
        "#emonews",
        "#thaimoji",
        "#cyberbully",
        "#longan_sentence",
        "#longan_tagger",
        "#longan_tokentag",
        "#longan_tokenizer",
        "#en2th_aligner",
        "#ch2th_aligner",
        "#tts",
        "#vajatts",
        "#textsum",
    ]

    matched_command = None
    for cmd in command_list:
        if user_input.startswith(cmd):
            matched_command = cmd
            break

    if matched_command:
        content = user_input[len(matched_command) :].strip()

        if matched_command == "#trexplus":
            result = tokenizer.tokenize(content, engine="trexplus", return_json=True)
            send_message(event, str(result))

        elif matched_command == "#lexto":
            result = tokenizer.tokenize(content, engine="lexto", return_json=True)
            send_message(event, str(result))

        elif matched_command == "#trex++":
            result = tokenizer.tokenize(content, engine="trexplusplus", return_json=True)
            send_message(event, str(list(zip(result["words"], result["tags"]))))

        elif matched_command == "#tner":
            result = ner.analyze(content, return_json=True)
            send_message(event, str(list(zip(result["words"], result["POS"], result["tags"]))))

        elif matched_command == "#longan_sentence":
            result = sentence_tokenizer.tokenize(content)
            send_message(event, str(result))

        elif matched_command == "#longan_tagger":
            result = tagger.tag(content)
            send_message(event, str(result))

        elif matched_command == "#longan_tokentag":
            result = token_tagger.tokenize_tag(content)
            send_message(event, str(result))

        elif matched_command == "#longan_tokenizer":
            result = logan_tokenizer.tokenize(content)
            send_message(event, str(result))

        elif matched_command == "#g2p":
            result = g2p.analyze(content)["output"]["result"]
            send_message(event, str(result))

        elif matched_command == "#textsum":
            print("Create function for Text summarization")
            # result = callTextSummarization(content)
            # send_message(event, str(result))

        elif matched_command == "#soundex":
            matched = re.match(r"#soundex(?:_([a-zA-Z0-9]+))?(.*)", user_input)
            if matched:
                # Default model, model = personname, royin
                model = matched.group(1) if matched.group(1) else "personname"
                content = matched.group(2).strip()

                result = soundex.analyze(content, model=model)["words"]
                send_message(event, str(result))

        elif matched_command.startswith("#thaiwordsim"):
            matched = re.match(r"#thaiwordsim(?:_([a-zA-Z0-9]+))?(.*)", user_input)
            if matched:
                # default to thwiki,  model = thwiki, twitter
                model = matched.group(1) if matched.group(1) else "thwiki"
                content = matched.group(2).strip()
                result = similarity.similarity(content, engine="thaiwordsim", model=model)
                send_message(event, str(result))

        elif matched_command == "#wordapprox":
            matched = re.match(r"#wordapprox(?:_([a-zA-Z0-9]+))?(.*)", user_input)
            if matched:
                # default to personname,  model = personname, royin, food
                model = matched.group(1) if matched.group(1) else "personname"
                content = matched.group(2).strip()

                result = similarity.similarity(
                    content, engine="wordapprox", model=model, return_json=True
                )
                send_message(event, str(result))

        elif matched_command == "#textclean":
            result = text_cleansing.clean(content)
            send_message(event, str(result))

        elif matched_command == "#tagsuggest":
            result = tag.analyze(content, numtag=5)
            send_message(event, str(result))

        elif matched_command == "#mtch2th":
            result = zh2th.translate(content, return_json=True)
            # result = Chainess2Thai(content, "zh", "th")
            send_message(event, str(result))

        elif matched_command == "#mtth2ch":
            result = th2zh.translate(content, return_json=True)
            # result = Chainess2Thai(content, "th", "zh")
            send_message(event, str(result))

        elif matched_command == "#mten2th":
            result = en2th.translate(content)
            # result = translate_xiaofan(content, "en2th")
            send_message(event, str(result))

        elif matched_command == "#mtth2en":
            result = th2en.translate(content)
            # result = translate_xiaofan(content, "th2en")
            send_message(event, str(result))

        elif matched_command == "#ssense":
            result = sentiment.analyze(content, engine="ssense")
            send_message(event, str(result))

        elif matched_command == "#emonews":
            result = sentiment.analyze(content, engine="emonews")
            send_message(event, str(result))

        elif matched_command == "#thaimoji":
            result = sentiment.analyze(content, engine="thaimoji")
            send_message(event, str(result))

        elif matched_command == "#cyberbully":
            result = sentiment.analyze(content, engine="cyberbully")
            send_message(event, str(result))

        elif matched_command == "#en2th_aligner":
            # # ตัวอย่างภาษาอังกฤษ-ไทย เช่น "I like to recommend my friends to Thai restaurants|ฉันชอบแนะนำเพื่อนไปร้านอาหารไทย"
            contents = content.split(
                "|"
            )  # รับข้อความจาก Line ในรูปแบบคู่ภาษาที่ต้องการจับคู่ ด้วยเครื่องหมาย "|"
            result = en_alignment.analyze(contents[0], contents[1], return_json=True)
            send_message(event, str(result))

        elif matched_command == "#ch2th_aligner":
            # # ตัวอย่างภาษาจีน-ไทย เช่น "我是10月10日从泰国来的。|ฉันมาจากประเทศไทยเมื่อวันที่ 10 เดือนตุลาคม"
            contents = content.split(
                "|"
            )  # รับข้อความจาก Line ในรูปแบบคู่ภาษาที่ต้องการจับคู่ ด้วยเครื่องหมาย "|"
            result = zh_alignment.analyze(contents[0], contents[1], return_json=True)
            send_message(event, str(result))

        elif matched_command == "#vajatts":
            speaker = 0  # [0=เสียงผู้ชาย, 1=เสียงผู้หญิง, 2=เด็กผู้ชาย, 3=เด็กผู้หญิง]
            tts.convert(content, cfg.DIR_FILE + cfg.WAV_FILE, speaker=speaker)

            audio_url = cfg.WAV_URL + cfg.DIR_FILE + cfg.WAV_FILE
            audio_duration = get_wav_duration_in_ms(cfg.DIR_FILE + cfg.WAV_FILE)

            audio_message = AudioSendMessage(
                original_content_url=audio_url, duration=audio_duration
            )
            send_audio_message(event, audio_message)

        elif matched_command == "#tts":
            speaker = 3
            response = callVaja9(content, speaker)
            # print(response.text)
            if response.json()["msg"] == "success":
                download_and_play(response.json()["wav_url"])
                audio_url = cfg.WAV_URL + cfg.DIR_FILE + cfg.WAV_FILE
                # print(f'URL: {audio_url}') ## Check URL send to Line API
                duration_ms = int(response.json()["durations"] * 1000)
                audio_message = AudioSendMessage(
                    original_content_url=audio_url, duration=duration_ms
                )
                send_audio_message(event, audio_message)
            else:
                send_message(event, "TTS failed")
    else:
        # echo(event)
        send_message(event, "Service not found")


def echo(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


# function for sending audio message
def send_audio_message(event, audio_message):
    line_bot_api.reply_message(event.reply_token, audio_message)


# function for sending message
def send_message(event, message):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


def get_wav_duration_in_ms(file_path):
    with wave.open(file_path, "r") as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = int(frames / rate) * 1000  # Convert seconds to milliseconds
        return duration


# Function call Vaja9
def callVaja9(text, speaker):
    url = cfg.URL_VAJA

    headers = {"Apikey": cfg.AIFORTHAI_APIKEY, "Content-Type": "application/json"}
    data = {"input_text": text, "speaker": speaker}
    response = requests.post(url, json=data, headers=headers)
    return response


# Function for download audio file
def download_and_play(sWav_url):
    file_name = cfg.DIR_FILE + cfg.WAV_FILE
    with open(file_name, "wb") as a:
        resp = requests.get(sWav_url, headers={"Apikey": cfg.AIFORTHAI_APIKEY})
        if resp.status_code == 200:
            a.write(resp.content)
        else:
            print(resp.reason)
            exit(1)


# Function for call Partii
def callPartii(file):
    url = cfg.URL_PARTII

    files = {"wavfile": (file, open(file, "rb"), "audio/wav")}

    headers = {
        "Apikey": cfg.AIFORTHAI_APIKEY,
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }

    param = {"outputlevel": "--uttlevel", "outputformat": "--txt"}
    response = requests.request("POST", url, headers=headers, files=files, data=param)
    data = json.loads(response.text)
    return data["message"]


# Function call Chinese to Thai/ Thai to Chinese
def Chainess2Thai(text, src, tar):
    url = "https://api.aiforthai.in.th/xiaofan-zh-th"

    payload = json.dumps({"input": text, "src": src, "trg": tar})
    headers = {"apikey": cfg.AIFORTHAI_APIKEY, "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.json())
    return response.json()["output"]


# Function call English to Thai/ Thai to English
def translate_xiaofan(text, direction):
    # direction = 'en2th' or 'th2en'
    url = f"https://api.aiforthai.in.th/xiaofan-en-th/{direction}"

    # Payload key changes based on direction
    if direction in ["en2th", "th2en"]:
        payload = json.dumps({"text": text})
    else:
        raise ValueError("Invalid direction. Use 'en2th' or 'th2en'.")

    headers = {"apikey": cfg.AIFORTHAI_APIKEY, "Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=payload)
    return response.json()["translated_text"]  # or response.text if you prefer raw


# End of  file
