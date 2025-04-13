from flask import Flask, render_template, request
import wikipedia
from googlesearch import search
from newspaper import Article

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form['query']

    
    try:
        wiki_summary = wikipedia.summary(query, sentences=2)
        wiki_url = wikipedia.page(query).url
    except:
        wiki_summary = "No Wikipedia summary found."
        wiki_url = ""

    
    results = []
    for url in search(query, num_results=10):  
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            results.append({
                'title': article.title,
                'summary': article.summary[:300] + "...",
                'link': url
            })
        except:
            continue

    return render_template('results.html', wiki_summary=wiki_summary, wiki_url=wiki_url, results=results)

if __name__ == '__main__':
    app.run(debug=True)
