import os
from dotenv import load_dotenv

load_dotenv()
file_path = "prev_count.txt"


def read_prev_count():
    """Read the previous count from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return int(file.read())
    else:
        return 0


def write_prev_count(count):
    """Write the updated count to a file."""
    with open(file_path, "w") as file:
        file.write(str(count))


config = {
    "WEBHOOK_URL": os.getenv("DISCORD_WEBHOOK_URL"),
    "COOKIE": os.getenv("COOKIE"),
    "BASE_API_URL": os.getenv("BASE_API_URL"),
    "PREV_NOTICES_COUNT": read_prev_count(),
    "ROLE_ID": os.getenv("ROLE_ID"),
}
