# Telegram Video Note Bot 🎥⭕

A simple and portable Telegram bot that converts regular videos into rounded Telegram Video Notes (circles). Built with Python, `aiogram` 3.x, and a portable version of FFmpeg.

## Features
* **Auto-Cropping:** Automatically crops the input video to a perfect 1:1 square (centered) to meet Telegram's requirements.
* **Auto-Trimming:** Trims videos longer than 60 seconds (Telegram's limit for video notes).
* **High Portability:** Uses `imageio-ffmpeg`, meaning FFmpeg binaries are downloaded automatically via pip. No need to manually install FFmpeg on your operating system!
* **Fast Processing:** Optimized FFmpeg settings (`-preset fast`, `-crf 28`) for a good balance between speed, quality, and file size.

## Requirements
* Python 3.8 or higher
* A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
   cd YourRepoName
Create and activate a virtual environment:

Windows:

Bash
python -m venv venv
venv\Scripts\activate
Linux/macOS:

Bash
python3 -m venv venv
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt


4. **Configure the Bot:**
   * Open `main.py`
   * Replace the `TOKEN` variable with your actual Telegram Bot API token. *(Note: For production, it's recommended to use environment variables like `.env` to store your token securely).*

5. **Run the Bot:**
   ```bash
   python main.py
   
Limitations
File Size: The standard Telegram Bot API only allows bots to download files up to 20 MB. If a user sends a video larger than 20 MB, the bot will notify them about the limit.

Built With
aiogram 3 - Asynchronous framework for Telegram Bot API.

imageio-ffmpeg - Portable FFmpeg wrapper for Python.