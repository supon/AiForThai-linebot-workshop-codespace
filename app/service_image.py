import requests
from aift import setting
from aift.image import super_resolution
from aift.image.classification import chest_classification, nsfw, violence_classification
from aift.image.detection import face_blur
from fastapi import APIRouter, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    ImageMessage,
    ImageSendMessage,
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from app.configs import Configs

router = APIRouter(tags=["Image"], prefix="/image")

cfg = Configs()

setting.set_api_key(cfg.AIFORTHAI_APIKEY)  # AIFORTHAI_APIKEY
line_bot_api = LineBotApi(cfg.LINE_CHANNEL_ACCESS_TOKEN)  # CHANNEL_ACCESS_TOKEN
handler = WebhookHandler(cfg.LINE_CHANNEL_SECRET)  # CHANNEL_SECRET

######### Dictionary to store user's previous text messages #####
user_messages = {}


@router.post("")
async def image_demo(request: Request):
    """
    Line Webhook endpoint สำหรับรับข้อความและรูปภาพจาก Line Messaging API และประมวลผลด้วย AI FOR THAI

    ฟังก์ชันนี้ทำหน้าที่:
    1. รับ HTTP POST Request จาก Line Webhook
    2. ตรวจสอบลายเซ็น (X-Line-Signature) เพื่อยืนยันความถูกต้องของข้อความ
    3. ส่งข้อความไปยัง handler เพื่อประมวลผลอีเวนต์ที่ได้รับ
    4. รองรับการประมวลผลข้อความ (TextMessage) และรูปภาพ (ImageMessage):
        - สำหรับข้อความ (TextMessage): ใช้ข้อความเพื่อเลือกโมเดล AI เช่น Face Blur, Chest X-Ray Classification, NSFW Detection เป็นต้น
        - สำหรับรูปภาพ (ImageMessage): ประมวลผลรูปภาพด้วยโมเดล AI ที่เลือกไว้ และส่งผลลัพธ์กลับไปยังผู้ใช้
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode("UTF-8"), signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token or channel secret.")
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_messages[event.source.user_id] = event.message.text

    text = "Welcome to AIFT-CV model demo, please type following number \n to select the model \n 1.face_blur \n 2.chestXray \n 3.Violent \n 4.NFSW \n 5.Super_resolution"

    # return text response
    send_message(event, text)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_id = event.message.id
    image_content = line_bot_api.get_message_content(message_id)

    # Save the image locally and process it XXXs
    with open("image.jpg", "wb") as f:
        for chunk in image_content.iter_content():
            f.write(chunk)

    #### Extract previous text messages from user adasd###
    user_id = event.source.user_id
    previous_text = user_messages.get(user_id)
    previous_text = str(previous_text)

    if previous_text == "1":
        result = face_blur.analyze("image.jpg")
        result_url = result["URL"]
        send_image(event, result_url)
    elif previous_text == "2":
        result = chest_classification.analyze("image.jpg", return_json=False)
        result_text = result[0]["result"]
        send_message(event, result_text)
    elif previous_text == "3":
        result = violence_classification.analyze("image.jpg")
        result_text = result["objects"][0]["result"]
        send_message(event, result_text)
    elif previous_text == "4":
        result = nsfw.analyze("image.jpg")
        result_text = result["objects"][0]["result"]
        send_message(event, result_text)
    elif previous_text == "5":
        result = super_resolution.analyze("image.jpg")
        result_url = result["url"]
        send_image(event, result_url)

    elif previous_text == "6":
        result = person_detection(cfg.AIFORTHAI_APIKEY, "image.jpg")
        send_image(event, result)

    else:
        send_message(event, "Please type the number first")


def echo(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


# function for sending message
def send_message(event, message):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


## function for sending result
def send_image(event, image_url):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url=image_url, preview_image_url=image_url),
    )


##### function for convert http into https ####
def convert_http_to_https(url):
    """
       Converts a given URL from HTTP to HTTPS.

    Args:
      url: The URL string to be converted.

    Returns:
      The URL string with "http://" replaced by "https://".
      If the URL already starts with "https://", it remains unchanged.
    """
    if url.startswith("http://"):
        return url.replace("http://", "https://", 1)
    else:
        return url


#### function for person detection api for aiforthai ####
def person_detection(AIFORTHAI_APIKEY, image_dir):
    url = "https://api.aiforthai.in.th/person/human_detect/"
    files = {"src_img": open(image_dir, "rb")}  ### input image dir here ###
    data = {"json_export": "true", "img_export": "true"}
    headers = {"Apikey": AIFORTHAI_APIKEY}

    response = requests.post(url, files=files, headers=headers, data=data)
    response = response.json()["human_img"]
    response = convert_http_to_https(response)
    return response
