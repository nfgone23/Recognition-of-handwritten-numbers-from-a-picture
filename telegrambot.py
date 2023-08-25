import logging
# import main functions
from main import mnist_predict_img, numbers_extract, img_to_str
# import keras to make the main file work
import keras
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    ApplicationBuilder
)
from io import BytesIO
import numpy as np

# TOKEN
TOKEN = '6602981268:AAFH_ch6KdamaYQzvqOtk2yua7yHX-5mUH4'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

SKIP, PHOTO = range(2)

# functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboards = [["Recognize text on image"]]
    await update.message.reply_text(
        "Choose  <Recognize text on image>",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboards, one_time_keyboard=True, input_field_placeholder= "Recognize"
        )
    )
    return SKIP
async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Send me a photo for Optical character recognition.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("image.png")
    numbers_extract("image.png")
    model = keras.models.load_model('mnist_model.keras')
    s_out = img_to_str(model, "image.png")
    await update.message.reply_text(
        "Recognized text: " + str(s_out)
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "This is it.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SKIP: [MessageHandler(filters.Regex("^(Recognize text on image)$"), skip)],
            PHOTO: [MessageHandler(filters.PHOTO, photo)],
        },
        fallbacks=[CommandHandler("cancel",cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()