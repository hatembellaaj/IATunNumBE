#pip install -U flask-cors
import subprocess
from flask import Flask, request, render_template, send_file
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def videoToText():
        # handle the POST request
    if request.method == 'POST':
        
        videourl = request.form.get('videourl')
 
        #namevideo = videourl.split('/')[-1]
        strWav = 'yt-dlp -xv --ffmpeg-location /root/anaconda3/bin/ffmpeg --audio-format wav  -o lecun.wav -- \'' + videourl + '\''
        #strWav = 'yt-dlp -xv --ffmpeg-location /opt/homebrew/bin/ffmpeg --audio-format wav -o audio.wav -- \'' + videourl + '\''
        res = subprocess.Popen(strWav, shell=True, stdout=subprocess.PIPE).stdout.read()
        print("audio file created : ",res)
        return render_template ("loading.html")


    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>videourl: <input type="text" name="videourl"></label></div>
                <div><select name="language" id="language">
                <option value="fr">fr</option>
                <option value="en">en</option>
                <option value="ar">ar</option>
                </select></div>
               <input type="submit" value="Submit">
           </form>'''

@app.route('/task', methods=['POST', 'GET'])
def task():
    print("into task ")
    strWhisper = 'whisper audio.wav  --model small'
    subprocess.Popen(strWhisper, shell=True, stdout=subprocess.PIPE).stdout.read()
    return send_file('audio.txt')


