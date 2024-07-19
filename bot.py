import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from BotFather
BOT_TOKEN = '7266834196:AAEsON6SPIMuX_YQ0ZFRzh1s_GBNO9Jqjn0'
GROUP_CHAT_ID = '4227292082'  

# Define the list of meme tokens
TOKENS = {
    'blub': {'symbol': 'BLUB', 'name': 'Blub'},
    'liquor': {'symbol': 'LIQ', 'name': 'Liquor'},
    'pup': {'symbol': 'PUP', 'name': 'Pup'}
    'hsui': {'symbol': 'HSUI', 'name': 'Suicune'}
    # Add more tokens as needed
}

# Function to fetch market cap and buy data for a specific token
def fetch_token_data(token_symbol):
    sui_rpc_url = 'https://fullnode.mainnet.sui.io:443'  # Mainnet RPC URL
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sui_getLatestCheckpointSequenceNumber",
        "params": []
    }

    response = requests.post(sui_rpc_url, json=payload)
    data = response.json()
return {
    market_cap = data.get('result', {}).get('market_cap', 'N/A')
    latest_buy = data.get('result', {}).get('latest_buy', 'N/A')
    buyer = data.get('result', {}).get('buyer', 'N/A')
    price = data.get('result', {}).get('price', 'N/A')
    image_url = data.get('result', {}).get('image_url', 'URL_OF_THE_IMAGE')  # Replace with actual key if available
    }

# Define a command handler function
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Wassup! I'm your DEGEN bot to track memes in the Sui Network.')

# Function to handle specific token commands dynamically
def token_command(update: Update, context: CallbackContext) -> None:
    token_symbol = context.args[0].lower() if context.args else None
    if token_symbol and token_symbol in TOKENS:
        data = fetch_token_data(TOKENS[token_symbol]['symbol'])
        market_cap_message = (
            f"Token: {TOKENS[token_symbol]['name']}\n"
            f"Market Cap: {data['market_cap']}\n"
            f"Price: {data['price']}"
        )
        update.message.reply_text(market_cap_message)
    else:
        update.message.reply_text('Token not found or not specified. Usage: /token <token_symbol>')

# Function to post buy updates for all tokens to the group with images
def post_buy_update(context: CallbackContext) -> None:
    for token_symbol, token_info in TOKENS.items():
        data = fetch_token_data(token_info['symbol'])
        buy_message = (
            f"New Buy!\n"
            f"Token: {token_info['name']}\n"
            f"Size: {data['latest_buy']}\n"
            f"Buyer: {data['buyer']}\n"
            f"Market Cap: {data['market_cap']}\n"
            f"Price: {data['price']}"
        )
        context.bot.send_message(chat_id=GROUP_CHAT_ID, text=buy_message)
        if 'image_url' in data and data['image_url']:
            context.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=data['image_url'])

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("token", token_command))

    # Set up a job to post buy updates periodically (e.g., every 10 minutes)
    job_queue = updater.job_queue
    job_queue.run_repeating(post_buy_update, interval=600, first=0)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
