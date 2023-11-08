#pip install -U flask-cors
import subprocess
import os
import shutil
from flask import Flask, request, render_template, send_file
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def videoToText():
        # handle the POST request
    if request.method == 'POST':
        
        videourl = request.form.get('videourl')
        language = request.form.get('language')
        translateto = request.form.get('translateto')
        model=request.form.get('model')
 
        #namevideo = videourl.split('/')[-1]
        strWav = 'yt-dlp -xv --ffmpeg-location /root/anaconda3/bin/ffmpeg --audio-format wav  -o audio.wav -- \'' + videourl + '\''
        #strWav = 'yt-dlp -xv --ffmpeg-location /opt/homebrew/bin/ffmpeg --audio-format wav -o audio.wav -- \'' + videourl + '\''
        res = subprocess.Popen(strWav, shell=True, stdout=subprocess.PIPE).stdout.read()
        print("audio file created : ",res)
        return render_template ("loading.html", language=language, translateto=translateto, model=model)


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
                <option value="ru">ru</option>
                </select></div>
                <div><label>TRANSLATE TO: (NOT YET DONE - Only english language is supported)</label><select name="translateto" id="translateto">
                <option value="en" selected="selected">en</option>
                <option value="fr">fr</option>
                <option value="ar">ar</option>
                </select></div>

                <div><label>MODEL: </label><select name="model" id="model">
                <option value="tiny">tiny - 39M</option>
                <option value="base" selected="selected">base - 74M</option>
                <option value="small">small - 244M</option>
                <option value="medium">medium - 769M</option>
                <option value="large">large - 1550M</option>
                <option value="large-v2">large-v2 - 1550M</option>
                </select></div>

               <input type="submit" value="Submit">
           </form>'''

@app.route('/task/<language>/<translateto>/<model>', methods=['POST', 'GET'])
def task(language,translateto,model):
    print("into task : language : ", language)
    print("into task : translateto : ", translateto)
    print("into task : model : ", translateto)
    translateto=""
    if(translateto==""):
        strWhisper = 'whisper audio.wav  --language '+ language + ' --model ' + model
    else:
        strWhisper = 'whisper audio.wav --task transcribe '+ translateto +' --language '+ language + ' --model ' + model

    
    print("strWhisper : ",strWhisper)
    subprocess.Popen(strWhisper, shell=True, stdout=subprocess.PIPE).stdout.read()


    # Dossier source contenant les fichiers
    dossier_source = '.'

    # Dossier de destination où vous voulez déplacer les fichiers
    dossier_destination = './uploads'

    # Liste tous les fichiers dans le dossier source
    fichiers_source = os.listdir(dossier_source)

    # Parcourt la liste des fichiers
    for fichier in fichiers_source:
        # Vérifie si le nom du fichier commence par "audio"
        if fichier.startswith('audio'):
            # Chemin complet du fichier source
            chemin_source = os.path.join(dossier_source, fichier)
            # Chemin complet du fichier de destination (incluant le nom du fichier)
            chemin_destination = os.path.join(dossier_destination, fichier)
            # Déplace le fichier vers le dossier de destination
            shutil.move(chemin_source, chemin_destination)
            print(f'Fichier {fichier} déplacé avec succès vers {dossier_destination}')

    return home() #send_file('audio.txt')

# Page d'accueil avec le formulaire pour l'upload
@app.route('/home')
def home():
    files = os.listdir('uploads')  # Liste des fichiers dans le dossier "uploads"
    return render_template('index.html', files=files)

# Route pour gérer l'upload de fichier
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save('uploads/' + uploaded_file.filename)  # Enregistre le fichier dans le dossier "uploads"
        return home() #'Fichier uploadé avec succès : ' + uploaded_file.filename
    else:
        return 'Aucun fichier sélectionné'

# Route pour télécharger un fichier
@app.route('/download/<filename>')
def download_file(filename):
    return send_file('uploads/' + filename, as_attachment=True)


