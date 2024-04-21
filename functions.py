import feedparser
from bs4 import BeautifulSoup
from llama_cpp.llama import Llama, LlamaGrammar
import json
import lorem

intercept_rss = "https://theintercept.com/feed/?lang=en"

def fetch_articles(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        title_soup = BeautifulSoup(entry.title, 'html.parser')
        content_soup = BeautifulSoup(entry.content[0]['value'], 'html.parser')
        article = {
            'title': title_soup.get_text(), 
            'content': content_soup.get_text()} 
        articles.append(article)
    return articles

def humorize(articles, prompt):
    i=0
    humorized = []    
    llm = Llama(
        model_path = "D:\GGUF\Hermes-2-Pro-Mistral-7B.Q8_0.gguf", 
        chat_format = "chatml", 
        n_ctx = 8192, 
        n_gpu_layers = 0)
    
    grammar = LlamaGrammar.from_file("humorized.gbnf")

    for piece in articles:
        prompt = prompt + "\n\n Title: \n" + str(piece['title']) + "\n\n Content:" + str(piece['content'])
        output = llm(prompt=prompt, grammar=grammar, max_tokens=8192)
        output = json.loads(output['choices'][0]['text'])
        article = {'id': i,
                   'title': output['Funny_Title'],
                    'content': output['Funny_Content']
                    }
        humorized.append(article)
        i +=1
    return humorized

def humorize_debug(articles, prompt):
    i=0
    humorized = []    

    for piece in articles:
        article = {'id': i,
                   'title': lorem.sentence(),
                    'content': lorem.text()
                    }
        i+=1
        humorized.append(article)
    return humorized
