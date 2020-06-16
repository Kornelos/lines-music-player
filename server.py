import os
from flask import Flask
from flask import render_template, request
from player import MusicPlayer
from werkzeug.utils import secure_filename
from flask import send_file
#from gpio_handler import GpioHandler
from subprocess import call
import signal
from sys import exit
# creates a Flask application, named app
app = Flask(__name__)
player = MusicPlayer()

def signal_handler(sig, frame):
    print("Stopping..")
    player.stop()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

@app.route("/")
def index(msg='Click next/prev to start playing'):
    songs = player.get_songs()
    return render_template('index.html',song_list = songs,ret_msg=msg)

# play related methods
@app.route("/next/", methods=['POST'])
def next_song():
    player.next_song()
    return index("next song playing")

@app.route("/prev/", methods=['POST'])
def prev_song():
    player.prev_song()
    return index("prev song playing")

@app.route("/stop/",methods=['POST'])
def stop_song():
    player.pause()
    return index("song (un)paused")

@app.route("/soundUp/",methods=['POST'])
def sound_up():
    call(["/usr/bin/amixer", "-M", "set", "Master", "9%+"])
    return "volume up"

@app.route("/soundDown/",methods=['POST'])
def sound_down():
    call(["/usr/bin/amixer", "-M", "set", "Master", "9%-"])
    return "volume up"

# file upload
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'mp3', 'ogg', 'wav'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods = ['POST'])
def upload_file():
    f = request.files['file']
    if allowed_file(f.filename):
        filename = secure_filename(f.filename)
        f.save(os.path.join('./songs/',filename))
        player.get_songs()
        player.load_song()
        return index('file uploaded successfully')
    else:
        return index("Wrong file extension")
# file download

@app.route('/download/',methods =['POST'])
def downloadFile ():
    f = request.json['filename']
    return send_file('./songs/'+f, as_attachment=True)
    
# run the application
if __name__ == "__main__":
    # init player
    player.get_songs()
    player.select_song(0)
    player.load_song()

    # run server
    app.run(host='0.0.0.0',port=8810)