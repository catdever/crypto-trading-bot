import requests
import os
from logger import logger
from load_config import *

config = load_config('config.yml')

telegram_enabled = "ENABLED" in config['TELEGRAM'] and config['TELEGRAM']['ENABLED']

if not telegram_enabled:
   logger.info('Telegram is disabled')
else:
   if "BOT_TOKEN" in config['TELEGRAM'] and "BOT_CHAT_ID" in config['TELEGRAM']:
      # read config
      bot_token = config['TELEGRAM']['BOT_TOKEN']
      bot_chatID = str(config['TELEGRAM']['BOT_CHAT_ID'])
      logger.info('Telegram initialized')
   else:
      # bail when config is not supplied
      logger.info('Telegram not configured -> disabled')
      telegram_enabled = False


def send_telegram(message, key = 'DEBUG'):
   """
   send_telegram sends a notification message to telegram

   :param message: the message to send
   :param key: message key, allows enabling/disabling of specific messages, defaults to DEBUG
   """ 

   # telegram is disabled, don't do anything
   if not telegram_enabled:
      return

   if key in config['TELEGRAM']['NOTIFICATIONS']:      
      if config['TELEGRAM']['NOTIFICATIONS'][key]:
         logger.debug(f'TELEGRAM sending {key} {message}')
         send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message   
         response = requests.get(send_text)
         if response.status_code != 200:
            logger.error(f'failed to send telegram message: {response.json()}')
   #    else:
   #       logger.info(f'Telegram message key {key} is disabled, not sending {message}')
   # else:
   #    logger.info(f'Telegram message key {key} is not configured, not sending {message}')
