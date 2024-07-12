import re
import json
import requests
import random
import markdownify
from config import config

notice_no = config["PREV_NOTICES_COUNT"]
WH_NORMAL_URL = config["WEBHOOK_URL"]
WH_ERROR_URL = config["WEBHOOK_ERROR_URL"]

emojis = [
    "🙇🏻",
    "👴🏻",
    "🫶🏻",
    "👍🏻",
    "😘",
    "🤠",
    "😉",
    "😇",
    "🤖",
    "👾",
    "🤡",
    "😸",
    "💫",
    "🤩",
    "🐻",
    "🪿",
    "🐼",
    "🦄",
    "🦬",
    "🐮",
    "🐶",
    "🎉",
    "🎊",
    "🧸",
    "🔥",
    "🌞",
    "🍀",
    "🍁",
    "🍄",
    "🦊",
    "🐛",
    "🐣",
    "😎",
]


def break_paragraph(paragraph, max_length=1900):
    paragraphs = []
    current_paragraph = ""
    current_length = 0

    for line in paragraph.splitlines():
        words = line.split()
        for word in words:
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length <= max_length:
                current_paragraph += word + " "
                current_length += word_length
            else:
                paragraphs.append(current_paragraph.strip())
                current_paragraph = word + " "
                current_length = word_length

        current_paragraph += "\n"  # preserve line breaks

    if current_paragraph.strip():  # append last paragraph
        paragraphs.append(current_paragraph.strip())

    return paragraphs


def send_discord_message(webhook_url, message):
    # Discord limits messages to 2000 characters, so split the message into chunks
    chunks = break_paragraph(message)

    for i, chunk in enumerate(chunks):
        data = {"content": chunk}

        headers = {"Content-Type": "application/json"}

        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

        if response.status_code == 204:
            print(f"Message part {i+1}/{len(chunks)} sent successfully.")
        else:
            print(
                f"Failed to send message part {i+1}/{len(chunks)}. Status code: {response.status_code}, Response: {response.text}"
            )


def send_msg(response):
    global notice_no
    data = response[0]["result"]["data"]
    random_emoji = random.choice(emojis)
    final_text = f"ㅤ\n\n{random_emoji} "
    final_text += f"<@&{config['ROLE_ID']}> \nNotice No: {notice_no}\n"
    final_text += f'**{data["title"]}**' + "\n\nㅤ"
    send_discord_message(WH_NORMAL_URL, final_text)
    final_text = ""
    html = data["body"]
    markdown_txt = markdownify.markdownify(html, heading_style="ATX")
    cleaned_text = re.sub(r"\n\s*\n", "\n\n", markdown_txt).strip()
    final_text += cleaned_text
    if data["attachments"]:
        attachment = data["attachments"]
        final_text += "\n\n"
        final_text += f'[{attachment[0]["name"]}]({attachment[0]["url"]})'
    notice_no += 1
    send_discord_message(WH_NORMAL_URL, final_text)


def send_error(error_msg):
    error_msg += "<@&1046045978802782288>\n\n"
    send_discord_message(WH_ERROR_URL, error_msg)
