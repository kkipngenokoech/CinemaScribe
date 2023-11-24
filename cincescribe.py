import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your Telegram Bot Token
TOKEN = "6914746363:AAG6TMIrudObbkkcv-dTQ_xmy4jI7G3xFIY"

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a video link, and I will provide its duration.')

# Function to handle incoming messages with video links
def handle_video_link(update: Update, context: CallbackContext) -> None:
    # Get the message text
    message_text = update.message.text

    # Extract video link from the message text
    video_link = extract_video_link(message_text)

    if video_link:
        # Get video duration using MoviePy
        duration = get_video_duration(video_link)

        # Reply with the video duration
        update.message.reply_text(f"The duration of the video is {duration} seconds.")
    else:
        update.message.reply_text("Please provide a valid video link.")

# Rest of your code...

# Main function to start the bot
def main() -> None:
    updater = Updater(TOKEN, update_queue=True)

    dp = updater.dispatcher

    # Add command handler for /start
    dp.add_handler(CommandHandler("start", start))

    # Add message handler for video links
    dp.add_handler(MessageHandler(filters.text & ~filters.command, handle_video_link))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
