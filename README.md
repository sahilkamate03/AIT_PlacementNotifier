# AIT Placement Notices to Discord

This project automates the process of sending notices from the AIT Placement website to a Discord channel using Discord Webhooks. Joint the discrod server to get the notifications. [Join Server](https://discord.gg/QfxuDbb2WU)

![Discrod Server Image](https://github.com/sahilkamate03/AIT_PlacementNotifier/blob/main/images/image.png?raw=true)

## Features

- Automatically fetches notices from the AIT Placement website.
- Sends the notices to a specified Discord channel using a webhook.
- Easy to set up and configure.

## Getting Started

### Prerequisites

- Python 3.11+
- Access to the AIT Placement website
- A Discord channel and webhook URL

### Installation (Linux)

1. Clone the repository:
   ```bash
   git clone https://github.com/sahilkamate03/AIT_PlacementNotifier.git
   cd AIT_PlacementNotifier
   ```
2. Create Virtual Environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the script:
   - Ensure you have access to the AIT Placement website.
   - Edit the `.env.example` and save it as `.env` for local development

### Usage

Run the script:

```bash
python index.py
```
