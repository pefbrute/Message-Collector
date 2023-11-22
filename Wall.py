from telethon import TelegramClient, events, sync
from datetime import datetime
import re
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

class MessageBatchProcessor:
    def __init__(self, batch_size=10, batch_interval=6):
        self.message_batch = []
        self.batch_size = batch_size
        self.batch_interval = batch_interval

    async def process_batch(self, client, chat_dict, keywords_re, channel_name):
        while True:
            current_time = datetime.now()
            if len(self.message_batch) >= self.batch_size or any(
                (current_time - event['timestamp']).seconds > 5 for event in self.message_batch):
                logging.info("Processing batch...")
                for event in self.message_batch:
                    if keywords_re.search(event['message'].raw_text):
                        try:
                            await event['message'].forward_to(channel_name)
                            channel_id = event['message'].message.peer_id.channel_id
                            await client.send_message(entity=channel_name, message=chat_dict[channel_id])
                        except KeyError as e:
                            logging.error(f"KeyError: {e} - Channel ID not found in chat_dict.")
                        except Exception as e:
                            logging.error(f"An unexpected error occurred: {e}")
                self.message_batch = []
            await asyncio.sleep(self.batch_interval)

# Your existing code for initialization
api_id = ID (You can take it from - https://my.telegram.org/auth)
api_hash = HASH (It from here too - https://my.telegram.org/auth)
channel_name = CHANNEL_NAME (Where to send messages)

keywords = ["менять", "меняю", "меняет", "менял", "меняйте", "обмен", "крипту", "крипта", "курс", "рупии", "руппи", "экскурсия", "экскурсии", "трансфер", "трансфером"]
keywords_re = re.compile(r'\b(?:{})\b'.format("|".join(re.escape(word) for word in keywords)), re.IGNORECASE)

chat_dict = {
    1720352497: "https://t.me/testing_group_roup",
    1503790351: "https://t.me/Shri_Lanka_RU",
    1122616041: "https://t.me/srilanka_forum",
    1676001373: "Шри-Ланка",
    1605996131: "https://t.me/+5r0wad3_-dBhYmYy",
    1595332067: "https://t.me/Shri_Lanka_Unawatuna",
    1465267513: "https://t.me/Shri_Lanka_Bentota",
    1537393491: "https://t.me/Shri_Lanka_Weligama",
    1458400705: "https://t.me/Shri_Lanka_timur_tours",
    1765562238: "https://t.me/Shri_Lanka_Mirissa",
    1328936495: "https://t.me/lankaru",
    1723102505: "https://t.me/srilanka_shri_lanka",
    1475806357: "https://t.me/srilanka_popytchiki_transfer",
    1646696794: "https://t.me/Sri_Lanka_Go",
    1535627250: "https://t.me/Shri_Lanka_Kandy",
    1178264087: "https://t.me/lankaxchange",
    1678234350: "https://t.me/srilanka_obmen"
}

client = TelegramClient('anon', api_id, api_hash)
batch_processor = MessageBatchProcessor()

@client.on(events.NewMessage(chats=tuple(chat_dict.keys())))
async def main(event):
    timestamped_event = {'message': event, 'timestamp': datetime.now()}
    batch_processor.message_batch.append(timestamped_event)

# Schedule the batch processing
client.loop.create_task(batch_processor.process_batch(client, chat_dict, keywords_re, channel_name))

client.start()

client.run_until_disconnected()
