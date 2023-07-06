import os
import openai
import pickle
import argparse
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List

load_dotenv() 

openai.api_type = "azure"
openai.api_base = "https://openai9-jj.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class History:
    question: str
    answer: str


class AI:
    
    history: List[History]

    def __init__(self, engine="apideployment"):
        self.engine = engine
        self.load_history()
        self.history_index = -1

    def use_proxy(self, use_proxy: bool):
        openai.proxy = {
            "http": os.getenv("OPENAI_PROXY"),
            "https": os.getenv("OPENAI_PROXY")
        } if use_proxy else ""
        

    def ask(self, question):
        try:
          response = openai.ChatCompletion.create(
            engine="apideployment",
            messages = [{"role":"system","content":f"{question}"}],
            temperature=0.5,
            max_tokens=4000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
          )
        except Exception as e:
          return "Error: " + str(e)
        
        response_text = response.choices[0].message.content.strip()
        self.history.append(History(question, response_text))
        self.save_history()
        return response_text
    
    def save_history(self):
        with open("history.bin", "wb") as file:
          pickle.dump(self.history, file)

    def load_history(self):
        try:
          with open("history.bin", "rb") as file:
            self.history = pickle.load(file)
        except:
            self.history = []

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-q', '--question', help='Question to ask')
  args = parser.parse_args()
  ai = AI()
  answ = ai.ask(args.question)
  print(answ)