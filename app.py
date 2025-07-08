from flask import Flask, render_template, request, jsonify
import os
from pytube import YouTube
import vlc
import threading
import time
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()
# VLC setup
instance = vlc.Instance()
player = instance.media_player_new()
current_track = {
    'title': '',
    'url': '',
    'is_playing': False
}
def play_audio(url):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        media = instance.media_new(audio_stream.url)
        player.set_media(media)
        player.play()
        
        current_track.update({
            'title': yt.title,
            'url': url,
            'is_playing': True
        })
        
        while player.get_state() not in [vlc.State.Ended, vlc.State.Error]:
            time.sleep(1)
            
