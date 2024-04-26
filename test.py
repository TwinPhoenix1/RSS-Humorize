from functions import *
from pydantic import BaseModel
import json

model_path = "D:\GGUF\Hermes-2-Pro-Mistral-7B.Q8_0.gguf" # enter your path to the model to use here
feeds = ["https://www.vox.com/rss/index.xml"]       # your list of RSS feeds 

prompt = """Rewrite the title and the content of the following news article in a humorous way while 
                maintaining factual accuracy. Cover all information provided in your humorous rewrite. 
                Here's the json schema you must adhere to: \n<schema>\n{schema}\n<schema>"""

class ThreadData(BaseModel):
    Funny_Title: str
    Funny_Content: str

schema = json.dumps(ThreadData.model_json_schema())
prompt = prompt.replace("{schema}", schema)

feeds = ["https://www.vox.com/rss/index.xml"]      
articles = scrape_articles(feeds)