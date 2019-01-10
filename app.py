from selenium import webdriver
from time import sleep
from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

def Twitter(usr,pwd,path,desc,speed):
    if usr:
        #browser
        driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        #URL
        driver.get('https://twitter.com/login')
        #USERNAME
        usr_box = driver.find_element_by_class_name('js-username-field')
        #sending username
        usr_box.send_keys(usr)
        #PASSWORD
        pwd_box = driver.find_element_by_class_name('js-password-field')
        #sending password
        pwd_box.send_keys(pwd)
        #LOGIN
        login_button = driver.find_element_by_css_selector('button.submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
        #clicking on login
        login_button.submit()

        #Wait until login
        sleep(speed)

        #ATTACH MEDIA
        image_box = driver.find_element_by_css_selector('input.file-input.js-tooltip')
        #sending media
        image_box.send_keys(path)

        #wait for a bit (until its uploaded to browser maybe )
        sleep(speed)

        #DESCRIPTION
        text_box = driver.find_element_by_id('tweet-box-home-timeline')
        #sending description
        text_box.send_keys(desc)
        #TWEET
        tweet_button = driver.find_element_by_css_selector('button.tweet-action.EdgeButton.EdgeButton--primary.js-tweet-btn')
        tweet_button.click()
        sleep(speed*1.5)
        driver.close()
        return
    pass

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():    
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def go():
    tun = request.form['tun']
    tup = request.form['tup']
    if tun is None or tup is None:
        tun = tup = ""

    file = request.files['media']
    filename = secure_filename(file.filename)
    media = os.path.abspath(filename)
    file.save(media)

    desc = request.form['desc']

    speed = int(request.form['speed'])

    Twitter(tun,tup,media,desc,speed)
    return '''
            <script>
            alert('Success :)');
            window.location = "/";
            </script>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=False,threaded=True)