import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from imageio_ffmpeg import get_ffmpeg_exe

# Insert your bot token here
TOKEN = "your_token"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "👋 **Hello! I'm your Video Note assistant.**\n\n"
        "Just send me any video, and I will:\n"
        "1. Crop it to a square (centered).\n"
        "2. Trim it to 60 seconds (if it's longer).\n"
        "3. Convert it into a Telegram video note (circle).\n\n"
        "💡 *Tip:* Try to send videos under 20 MB due to Telegram API limits."
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message(F.video)
async def handle_video(message: Message):
    # Check file size (20MB = 20 * 1024 * 1024 bytes)
    if message.video.file_size > 20 * 1024 * 1024:
        await message.answer("❌ The file is too large. Telegram allows bots to download videos up to 20 MB only.")
        return

    processing_msg = await message.answer("🔄 Processing video... Please wait.")
    
    input_path = f"input_{message.message_id}.mp4"
    output_path = f"output_{message.message_id}.mp4"

    try:
        # Download the video from Telegram
        file_info = await bot.get_file(message.video.file_id)
        await bot.download_file(file_info.file_path, input_path)

        # Get the path to the portable FFmpeg executable
        ffmpeg_exe = get_ffmpeg_exe()

        # FFmpeg command to crop, scale, and convert
        cmd = [
            ffmpeg_exe,
            '-y',
            '-i', input_path,
            '-t', '60',  
            '-vf', 'crop=min(iw\\,ih):min(iw\\,ih),scale=384:384',
            '-c:v', 'libx264',
            '-preset', 'fast', 
            '-crf', '28',      
            '-c:a', 'aac',
            '-b:a', '128k',
            output_path
        ]

        # Run FFmpeg asynchronously
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Get execution results
        stdout, stderr = await process.communicate()

        # If FFmpeg fails or the output file is not created
        if process.returncode != 0 or not os.path.exists(output_path):
            error_text = stderr.decode('utf-8')
            error_snippet = error_text[-1000:] if len(error_text) > 1000 else error_text
            
            await processing_msg.edit_text(
                f"❌ Error during video conversion.\n\nDeveloper details:\n<code>{error_snippet}</code>", 
                parse_mode="HTML"
            )
            return

        # Send the processed video note
        video_note = FSInputFile(output_path)
        await message.answer_video_note(video_note)
        await processing_msg.delete()

    except Exception as e:
        await processing_msg.edit_text(f"❌ An unexpected error occurred: {e}")
    finally:
        # Clean up temporary files
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

async def main():
    print("🚀 Bot started. Open Telegram and send /start")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())