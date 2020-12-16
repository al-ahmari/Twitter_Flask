from flask import Flask,render_template,request,redirect
import tweepy
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import numpy as np

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        print('this is GET')
        return render_template('forms.html')
    else:
        x=(request.form['word'])
        f = open('searches.txt','w')
        f.write(x)
        f.close()
        y=(request.form['number'])
        f2 = open('number.txt','w')
        f2.write(y)
        f2.close()
        WC()
        return render_template('forms.html')
        #print(request.form.get('location'))
    #return render_template('form.html') 
        
    


@app.route('/Output')
def WC():
    health = False
    f = open("searches.txt", "r")
    f2 = open("number.txt", "r")
    try:
        var = str(f.read())
        num = int(f2.read())
        health = True
    except:
        print('Please enter a correct word an number')
        num = -1
        health = False
    if num <1 or num >100:
        print('Please enter a positive number less than 100')
        return render_template('forms.html')
    #if health == False:
        #app.run(debug=True)

    consumer_key="s9DSe4ieigpCRablpK7QXEo4r"
    consumer_secret="EHc0V3jkNTeTSJ0UAJJLvrZTtbMuoOyxviR1NrnH41JiHAIo25"
    access_token="1031876113507803137-uiZDhJhAH8AlzmIsoyTSCURYBRDd8W"
    access_token_secret="E0xWxOQm7MkBBRMGMojDf4wB1caUoQd304ZcDxnibpBGm"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    
    api = tweepy.API(auth)
    #Erro_Messgae1= 'Please enter a number'
    #Erro_Messgae2= 'Please enter a number less than 100'
    No_Tweest = num
    query= api.search(q= var, lang= 'en',count= No_Tweest)
    f3= open ("temp.txt","wb")
    for info in query:
        print(info.text)
        f3.write(str(info.text).encode('cp1252', errors='ignore'))
        f3.write(b"\n")
    f3.close()

    f3= open ("temp.txt","r")
    words=f3.read()
    print(words)
    f3.close()


    fig = plt.figure()

    removed_words= ['covid19', 'covid 19', 'covid', 'RT', 'https', 'the', 'co', 'of', 'and', 'their',
                    'with', 'for', 't', 'i','to', 'at', 'is', 'a', 'in', 'are', 'This','amp', 'how',
                    'these', 'has', 'on', 'u', 'what', 'here', 'we','that', 's', 'we', 'by', 'you',
                    'have', 'about', 'they', 'will', 'it', 'if', 'can', 'be', 'more', 'please', 'our',
                    'your', 'an', 'as']

    wc = WordCloud(background_color="black", max_words=200, mask=None,
                stopwords=removed_words, contour_width=3, contour_color='steelblue').generate(words)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    fig.savefig('my_plot.png')
    return '''<img src='my_plot.png'>'''

if __name__ == "__main__":
        app.run(debug=True)