# from pygame import mixer
from os import listdir
#from gpio_handler import GpioHandler, BlinkTask
from mpd import MPDClient
SONGS_URL = 'http://0.0.0.0:8000/'
SONGS_DIR = 'songs/'
class MusicPlayer:
    #gpio = GpioHandler()
    current_song = ""
    songs = []
    paused = True
    def __init__(self):
        # mixer.init()
        self.mpc = MPDClient()
        self.mpc.connect("localhost",6600)
        #self.gpio.start_monitors()

    # load song list from filesystem
    def get_songs(self):
        self.songs = listdir(SONGS_DIR)
        return self.songs
    
    # select current playing song
    def select_song(self,song_num):
        if song_num > len(self.songs)-1:
            self.current_song = self.songs[0]
        else:
            self.current_song = self.songs[song_num]
    
    # load song into the player
    def load_song(self):
        # mixer.music.load(SONGS_DIR + self.current_song)
        print(self.current_song)
        self.mpc.clear()
        self.mpc.add(SONGS_URL + self.current_song)
        print('loaded song: ' + self.current_song)

    def next_song(self):
        index = self.songs.index(self.current_song)
        # if last go to first
        if index == len(self.songs)-1:
            self.current_song = self.songs[0]
        else:
            self.current_song = self.songs[index + 1]
        # play new song
        self.load_song()
        self.play()
        self.paused = False
    
    def prev_song(self):
        index = self.songs.index(self.current_song)
        # if first then go to last
        if index == 0:
            self.current_song = self.songs[len(self.songs)-1]
        else:
            self.current_song = self.songs[index -1]
        # play new song
        self.load_song()
        self.play()
        self.paused = False

    def play(self):
        # mixer.music.play()
        self.mpc.play()
        self.paused = False
        #self.gpio.start_blink()
        

    def pause(self):
        if self.paused:
            self.mpc.pause()
            self.paused = False
           # self.gpio.start_blink()
        else:
            # mixer.music.pause()
            self.mpc.pause()
            self.paused = True
           # self.gpio.stop_blink()


