from flask import Flask, render_template, request
import feedparser, datetime

articles = []
titles = []
sorted_t = []

months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

def get_titles(entries):
    t = []
    for item in entries:
        t.append(item['title'])
    return t

def get_details(entry):
    details = []
    details.append(entry['title'])
    
    for i,linka in enumerate(entry['links']):
        if 'image' in linka['type']:
            details.append(linka['href'])

    details.append(entry['published'])
    details.append(entry['summary'])
    details.append(entry['link'])
    return details

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('rss_reader.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   global articles
   global titles, sorted_t
   sorted_t = []
   if request.method == 'POST':
      result = request.form
      titles = []
      articles = []
      url = result.getlist('URL')[0]
      NewsFeed = feedparser.parse(url)
      entry = NewsFeed.entries
      t = get_titles(entry)
      for i,t in enumerate(t):
          titles.append((i,t))
      for item in entry:
           articles.append(get_details(item))
      return render_template("rss_result.html",result = titles, order = 0)

@app.route('/result/ordered')
def ordered_result():
   global titles
   global articles, sorted_t
   dates = []
   sorted_t = []
   for i,item in enumerate(articles):
       date = item[2]
       date = (date.split(',')[1]).split(' ')[1:-1]
       time = date[3].split(':')
       date_in_format = datetime.datetime(year=int(date[2]),month = months[date[1]], day = int(date[0]), hour = int(time[0]), minute = int(time[1]), second = int(time[2]))
       dates.append((i,date_in_format))
   sorted_by_time = sorted(dates,key=lambda x: x[1])[::-1]
   sorted_titles = []
   for item in sorted_by_time:
       idx = item[0]
       sorted_titles.append(titles[idx])
   sorted_t = sorted_titles
   
   return render_template("rss_result.html",result = sorted_titles, order = 1)
    
@app.route('/result/details/<int:idx>')
def article_details(idx):
    return render_template("rss_result_details.html",result = titles,data = articles[idx], order = 0, i = idx)

@app.route('/result/details/ordered/<int:idx>')
def article_details_ordered(idx):
    global sorted_t
    num = idx
    if sorted_t == []:
       dates = [] 
       for i,item in enumerate(articles):
           date = item[2]
           date = (date.split(',')[1]).split(' ')[1:-1]
           time = date[3].split(':')
           date_in_format = datetime.datetime(year=int(date[2]),month = months[date[1]], day = int(date[0]), hour = int(time[0]), minute = int(time[1]), second = int(time[2]))
           dates.append((i,date_in_format))
       sorted_by_time = sorted(dates,key=lambda x: x[1])[::-1]
       sorted_titles = []
       for item in sorted_by_time:
           id = item[0]
           sorted_titles.append(titles[id])
       sorted_t = sorted_titles

    return render_template("rss_result_details.html",result = sorted_t,data = articles[idx], order = 1, i = idx)
    
if __name__ == '__main__':
    app.run(debug=True)
 
