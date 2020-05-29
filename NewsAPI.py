import pickle
from bs4 import BeautifulSoup
import requests
import json
from sklearn.pipeline import Pipeline
from flask import Flask, send_from_directory
import os

app = Flask(__name__,static_folder='./Public')

with open('Modules/LogisticRegression.pickle','rb') as f:
    logisticRegression = pickle.load(f)
with open('Modules/vectorizer.pickle','rb') as f:
    vectorizer = pickle.load(f)
with open('Modules/encoder.pickle','rb') as f:
    encoder = pickle.load(f)

pipeline = Pipeline([
    ('Vectorizer',vectorizer),
    ('Classifier',logisticRegression)
])

def NewsJSON(query):
    url = 'https://www.bbc.co.uk/search?q=' + '+'.join(query.split(' ')) + '&sa_f=search-product&filter=news&suggid='
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,features='html.parser')
    headlines = soup.find_all('a',"css-118lm29-PromoLink ett16tt7")

    data = []
    for item in headlines:
        tag = item.find('span')
        news = {
            'title' : tag.text,
            'category' : encoder.inverse_transform(pipeline.predict([tag.text]))[0],
            'link' : item['href']
        }
        data.append(news)

    return json.dumps(data)

@app.route('/',defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    if path!= '':
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder , 'index.html')
        


@app.route('/news/<query>')
def news(query):
    print('query =',str(query),sep=' ')
    return NewsJSON(query)
    
@app.route('/news/')
def emptyquery():
    print('empty query')
    return json.dumps([{
        'status' : 'No response',
        'error' : 'Empty query'
    }])

if __name__ == '__main__':
   app.run()