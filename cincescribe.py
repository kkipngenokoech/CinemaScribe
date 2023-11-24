import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Application
from telegram import Update, ReplyKeyboardMarkup
from moviepy.editor import VideoFileClip

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your Telegram Bot Token
TOKEN = "6914746363:AAG6TMIrudObbkkcv-dTQ_xmy4jI7G3xFIY"

# Function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me a video link, and I will provide its duration.')

# Function to handle incoming messages with video links
def get_video_duration(video_link: str) -> int:
    try:
        # Download the video file
        clip = VideoFileClip(video_link)
        # Get the duration in seconds
        duration = int(clip.duration)
        return duration
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return 0  # Return 0 seconds in case of an error

def handle_command_choice(update: Update, context: CallbackContext) -> None:
    # Get the chosen command from the user
    chosen_command = update.message.text

    # Implement different actions based on the chosen command
    if chosen_command == "Get Duration":
        # Get video duration
        video_link = context.user_data.get("video_link")
        if video_link:
            duration = get_video_duration(video_link)
            update.message.reply_text(f"The duration of the video is {duration} seconds.")
        else:
            update.message.reply_text("Please provide a valid video link.")
    elif chosen_command == "Trim Video":
        # Implement video trimming logic (replace with your actual implementation)
        update.message.reply_text("You chose to trim the video. Implement your logic here.")
    # Add more conditions for other commands as needed

    # End the conversation or continue with other actions as needed
    context.user_data.pop("video_link", None)

def extract_video_link(message_text: str) -> str:
    # Replace this with your actual logic to extract the video link
    # For simplicity, this example assumes that the video link is the entire message text
    return message_text.strip()

async def handle_video_link(update: Update, context: CallbackContext) -> None:
    # Get the message text
    message_text = update.message.text

    # Extract video link from the message text
    video_link = extract_video_link(message_text)

    if video_link:
        # Save the video link to user_data for later use
        context.user_data["video_link"] = video_link

        # Send command menu
        commands = ["Get Duration", "Trim Video", "Another Command"]  # Add your actual commands here
        reply_markup = ReplyKeyboardMarkup([[command] for command in commands], one_time_keyboard=True)
        await update.message.reply_text("What would you like to do with the video?", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Please provide a valid video link.")

# Main function to start the bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Add command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Add message handler for video links
    filtersUsed = filters.TEXT & (~filters.COMMAND)
    application.add_handler(MessageHandler(filtersUsed, handle_video_link))

    # Add message handler for command choices
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_command_choice))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    # Run the bot until you send a signal to stop
    application.idle()

if __name__ == '__main__':
    main()
