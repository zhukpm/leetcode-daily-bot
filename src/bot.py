from datetime import datetime
from pydantic import BaseModel
import requests
from src.common import submission_link


LEETCODE_DAILY_GROUP_ID = '-1002270137956'


class Bot(BaseModel):
  token: str
  
  def api_url(self):
    return f"https://api.telegram.org/bot{self.token}/"

  def send_message(self, chat_id, message, useV2=False):
      if chat_id is None or message is None:
          return False

      params = {
          'chat_id': chat_id,
          'text': message,
          'disable_web_page_preview': True,
      }
      if useV2:
        params['parse_mode'] = 'MarkdownV2'
      res = requests.post(self.api_url() + "sendMessage", data=params).json()
      print(res)

      if res is None or 'result' not in res or 'message_id' not in res['result']:
          return None
      return res['result']['message_id']
    
    
def process_message(bot, db, data):
  try:
    message = data['message']
    chat_id = message['chat']['id']
    text = message['text']
    today = datetime.today().strftime('%Y-%m-%d')
    
    username = message['from']['username'] if 'username' in message['from'] else '😊'
    first_name = message['from']['first_name'] if 'first_name' in message['from'] else '😊'
    name = f'{first_name} ({username})'

    if text.startswith('/start') or text.startswith('/help'):
      bot.send_message(chat_id, "Please, send me a submission id for today's daily challenge")
    elif text.isnumeric():
      submission_id = text
    
    if submission_id.isnumeric():
      print(f"Will update submissions for {username} on {today}: {text}")
      result = db.submissions.update_one(
        {'username': name, 'date': today, 'chat_id': chat_id},
        {'$set': {'text': text}},
        True,
      )

      print(username, today, text, result)
      bot.send_message(chat_id, f"Updated submission for {today}: {submission_link(text)}")
      bot.send_message(LEETCODE_DAILY_GROUP_ID, f"New submission from {name}: {submission_link(text)}")
    else:
      bot.send_message(chat_id, "Incorrect input! please send me a submission id")
      raise ValueError(f"Incorrect link {data}")

  except Exception as e:
    print("Oops!")
    print(e)