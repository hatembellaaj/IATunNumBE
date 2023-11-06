#pip install -U flask-cors
import subprocess
from flask import Flask, request, render_template, send_file
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def videoToText():
        # handle the POST request
    if request.method == 'POST':
        
        videourl = request.form.get('videourl')
        language = request.form.get('language')
        translateto = request.form.get('translateto')
 
        #namevideo = videourl.split('/')[-1]
        strWav = 'yt-dlp -xv --ffmpeg-location /root/anaconda3/bin/ffmpeg --audio-format wav  -o audio.wav -- \'' + videourl + '\''
        #strWav = 'yt-dlp -xv --ffmpeg-location /opt/homebrew/bin/ffmpeg --audio-format wav -o audio.wav -- \'' + videourl + '\''
        res = subprocess.Popen(strWav, shell=True, stdout=subprocess.PIPE).stdout.read()
        print("audio file created : ",res)
        return render_template ("loading.html", language=language, translateto=translateto)


    # otherwise handle the GET request
    return '''
            <style>
                input[type=text], select {
                width: 100%;
                padding: 12px 20px;
                margin: 8px 0;
                display: inline-block;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
                }

                input[type=submit] {
                width: 100%;
                background-color: #4CAF50;
                color: white;
                padding: 14px 20px;
                margin: 8px 0;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                }

                input[type=submit]:hover {
                background-color: #45a049;
                }

                div {
                border-radius: 5px;
                background-color: #f2f2f2;
                padding: 20px;
                }
            </style>
           <form method="POST">
               <div><label>VIDEO URL: </label><input type="text" name="videourl"></div>
                <div><label>VIDEO LANGUAGE: </label><select name="language" id="language">
                <option value=""></option>
                <option value="fr">fr</option>
                <option value="en">en</option>
                <option value="ar">ar</option>
                </select></div>
                <div><label>TRANSLATE TO: (NOT YET DONE - Only english language is supported)</label><select name="translateto" id="translateto">
                <option value="en">en</option>
                <option value="fr">fr</option>
                <option value="ar">ar</option>
                </select></div>
               <input type="submit" value="Submit">
           </form>'''

@app.route('/task/<language>/<translateto>', methods=['POST', 'GET'])
def task(language,translateto):
    print("into task : language : ", language)
    print("into task : translateto : ", translateto)
    translateto=""
    if(translateto==""):
        strWhisper = 'whisper audio.wav  --language '+ language + ' --model small'
    else:
        strWhisper = 'whisper audio.wav --task transcribe '+ translateto +' --language '+ language + ' --model small'

    
    print("strWhisper : ",strWhisper)
    subprocess.Popen(strWhisper, shell=True, stdout=subprocess.PIPE).stdout.read()
    return send_file('audio.txt')


