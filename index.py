import requests
from config import config, write_prev_count
from discord import send_msg, send_error

BASE_API_URL = config["BASE_API_URL"]


def request_maker(url, notice_id=None):
    url = BASE_API_URL + url
    try:
        headers = {"Cookie": config["COOKIE"]}
        params = {}
        if notice_id is None:
            params = {
                "batch": 1,
                "input": '{"0":{"pageNos":1}}',
            }
        else:
            params = {
                "batch": 1,
                "input": f'{{"0":{{"id":"{notice_id}"}}}}',
            }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response = response.json()
        return response

    except Exception as e:
        send_error(str(e))
        print("Error running query:", e)


def worker(response):
    current_notices_count = response[0]["result"]["data"]["totalNotice"]
    if current_notices_count == 0:
        send_error("COOKIE expired !!")
        return

    prev_notices_count = config["PREV_NOTICES_COUNT"]
    if current_notices_count <= prev_notices_count:
        return
    notices = response[0]["result"]["data"]["notices"]
    pending_notices = current_notices_count - prev_notices_count

    for i in range(pending_notices):
        notice_id = notices[pending_notices - i]["id"]
        response = request_maker("notice.noticeDetail", notice_id=notice_id)
        send_msg(response)
        prev_notices_count += 1
        write_prev_count(prev_notices_count)


def run_query():
    response = request_maker("notice.publishedNoticeList")
    worker(response)


if __name__ == "__main__":
    run_query()
