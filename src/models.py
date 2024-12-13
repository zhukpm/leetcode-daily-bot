from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List
from collections import defaultdict
from src.common import submission_link
from random import randint



START_DATE = datetime(2024, 9, 16)


class DisplaySubmission(BaseModel):
  level: int
  url: str
  text: str
  
  
class Participant(BaseModel):
  name: str
  reputation: int
  submissions: List[DisplaySubmission]

  
def load_dummy_data():
  return [
    Participant(
      name="Bob Marley",
      reputation=55,
      submissions=[
        # week 1
        DisplaySubmission(level=4, text="Submission", url=""),
        DisplaySubmission(level=4, text="Submission", url=""),
        DisplaySubmission(level=1, text="Submission", url=""),
        DisplaySubmission(level=1, text="Submission", url=""),
        DisplaySubmission(level=0, text="Submission", url=""),
        DisplaySubmission(level=0, text="Submission", url=""),
        DisplaySubmission(level=0, text="Submission", url=""),

        # week 2
        DisplaySubmission(level=2, text="Submission", url=""),
        DisplaySubmission(level=2, text="Submission", url=""),
        DisplaySubmission(level=1, text="Submission", url=""),
        DisplaySubmission(level=5, text="Submission", url=""),
        DisplaySubmission(level=3, text="Submission", url=""),
        DisplaySubmission(level=4, text="Submission", url=""),
        DisplaySubmission(level=0, text="Submission", url=""),

      ],
    ).dict(),

    Participant(
      name="John McClane",
      reputation=45,
      submissions=[
        # week 1
        DisplaySubmission(level=4, text="Submission", url=""),
        DisplaySubmission(level=4, text="Submission", url=""),
        DisplaySubmission(level=1, text="Submission", url=""),
        DisplaySubmission(level=1, text="Submission", url=""),
        DisplaySubmission(level=0, text="Submission", url=""),
        DisplaySubmission(level=0, text="Submission", url=""),
        DisplaySubmission(level=0, text="Submission", url=""),

        # week 2
        DisplaySubmission(level=2, text="Submission", url=""),
        DisplaySubmission(level=2, text="Submission", url=""),
        DisplaySubmission(level=1, text="Submission", url=""),
        DisplaySubmission(level=5, text="Submission", url=""),
        DisplaySubmission(level=3, text="Submission", url=""),
        DisplaySubmission(level=4, text="Submission", url=""),
        DisplaySubmission(level=0, text="Submission", url=""),
        
      ],
    ).dict(),
  ]
  
  
def load_data_from_cursor(cursor):
  data = defaultdict(lambda: defaultdict(str))
  users = defaultdict(str)
  for record in cursor:
    k = record['chat_id'] if 'chat_id' in record else record['username']
    if 'username' in record:
      users[k] = record['username']
    data[k][record['date']] = record['text']
    
  
  start_date = START_DATE
  end_date = datetime.today()

  result = []
  days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
  for k, p in data.items():
    current_date = start_date
    submissions = []
    while current_date <= end_date:
        d = current_date.strftime("%Y-%m-%d")
        display_date = days_of_week[current_date.weekday()] + ", " + d
        if d in p:
          submissions.append(DisplaySubmission(level=4, text=display_date, url=submission_link(p[d])))
        else:
          submissions.append(DisplaySubmission(level=0, text=display_date, url=''))
        current_date += timedelta(days=1)

    result.append(Participant(name=users[k].split()[0], reputation=len(p), submissions=submissions).dict())
  
  result.sort(key=lambda p: (p['reputation'], randint(0, 100)), reverse=True)
  return result

def load_data(cursor=None, dummy=False):
  return load_dummy_data() if dummy else load_data_from_cursor(cursor)