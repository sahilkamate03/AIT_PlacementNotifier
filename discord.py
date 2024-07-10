import re
import json
import requests
import random
import markdownify
from config import config

emojis = ['🙇🏻','👴🏻','🫶🏻','👍🏻','😘','🤠','😉','😇','🤖','👾','🤡','😸','💫','🤩','🐻','🪿','🐼','🦄','🦬','🐮','🐶','🎉','🎊','🧸','🔥','🌞','🍀','🍁','🍄','🦊','🐛','🐣','😎']

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


def send_discord_message(message):
    webhook_url = config["WEBHOOK_URL"]
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
    data = response[0]["result"]["data"]
    random_emoji = random.choice(emojis)
    final_text = f"{random_emoji}\n\n"
    final_text += f"<@&{config['ROLE_ID']}> \nNotice No: {config["PREV_NOTICES_COUNT"]}\n\n"
    final_text += f'**{data["title"]}**' + "\n\n"
    send_discord_message(final_text)
    final_text = ""
    html = data["body"]
    markdown_txt = markdownify.markdownify(html, heading_style="ATX")
    cleaned_text = re.sub(r"\n\s*\n", "\n\n", markdown_txt).strip()
    final_text += cleaned_text
    if data["attachments"]:
        attachment = data["attachments"]
        final_text += "\n\n"
        final_text += f'[{attachment[0]["name"]}]({attachment[0]["url"]})'

    send_discord_message(final_text)
