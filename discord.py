import re
import json
import requests
import markdownify
from config import config


def send_discord_message(message):
    webhook_url = config["WEBHOOK_URL"]
    data = {"content": message}
    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(
            f"Failed to send message. Status code: {response.status_code}, Response: {response.text}"
        )


def send_msg(response):
    data = response[0]["result"]["data"]
    final_text = f"<@&{config['ROLE_ID']}> \n\n"
    final_text += f'**{data["title"]}**' + "\n\n"
    html = data["body"]
    markdown_txt = markdownify.markdownify(html, heading_style="ATX")
    cleaned_text = re.sub(r"\n\s*\n", "\n\n", markdown_txt).strip()
    final_text += cleaned_text
    if data["attachments"]:
        attachment = data["attachments"]
        final_text += "\n\n"
        final_text += f'[{attachment[0]["name"]}]({attachment[0]["url"]})'

    send_discord_message(final_text)
