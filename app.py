from functions import *
from datetime import timedelta
from flask import Flask, render_template, session
from flask_session import Session
from pydantic import BaseModel
import os
import json

# your path to the model to use here
model_path = "D:\GGUF\Hermes-2-Pro-Mistral-7B.Q8_0.gguf"  
# your list of RSS feeds (Vox only picked because it features full content in rss)
feeds = ["https://www.vox.com/rss/index.xml"]          

prompt = """Rewrite the title and the content of the following news article in a humorous way while 
                maintaining factual accuracy. Cover all information provided in your humorous rewrite. 
                Here's the json schema you must adhere to: \n<schema>\n{schema}\n<schema>"""

class ThreadData(BaseModel):
    Funny_Title: str
    Funny_Content: str

schema = json.dumps(ThreadData.model_json_schema())
prompt = prompt.replace("{schema}", schema)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

secret_key = os.urandom(12).hex()
app.secret_key = secret_key

@app.before_request
def session_setup():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)


@app.route('/')
def home():
    if 'content' in session: 
        humorized = session['content']
    else:
        articles = scrape_articles(feeds)
        articles = articles[:1]
        humorized = humorize(articles, prompt, model_path)
        session['content'] = humorized
    return render_template('index.html', humorized=humorized)

@app.route('/<int:article_id>')
def view_article(article_id):
    print('article_ID' + str(article_id) + '\n\n SESSION: \n\n' + str(session))
    for article in session['content']:
        if article['id'] == article_id:
            article_found = article
    print("OUTPUT \n\n TITLE: \n" + article_found['title'] + "\n\n CONTENT: \n" + article_found['content'])

    return render_template('post.html', article=article_found)

if __name__ == '__main__':
    app.run(debug=True)