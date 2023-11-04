#pip install -U flask-cors
import subprocess
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def videoToText():
        # handle the POST request
    if request.method == 'POST':
        videourl = request.form.get('videourl')
        strWav = 'yt-dlp -xv --ffmpeg-location /root/anaconda3/bin/ffmpeg --audio-format wav  -o lecun.wav -- \'' + videourl + '\''
        subprocess.Popen(strWav, shell=True, stdout=subprocess.PIPE).stdout.read()
        strWhisper = 'whisper lecun.wav  --model small' 
        res = subprocess.Popen(strWhisper, shell=True, stdout=subprocess.PIPE).stdout.read()
        return '''
                  <h1>The result is: {}</h1>'''.format(res)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>videourl: <input type="text" name="videourl"></label></div>
               <input type="submit" value="Submit">
           </form>'''



