from typing import NamedTuple
from pytube import YouTube, Playlist
from pytube.exceptions import PytubeError
import os
import random

class Music(NamedTuple):
    title : str = ""
    author : str = ""
    playlist : str = ""
    url : str = ""
    path : str = ""
    length : int = 0
    
class new_music:
    def __init__(self, video_url, title, author, playlist):
        print("-- new music", video_url, title, author, playlist)
        # Create a YouTube object
        self.yt = YouTube(video_url)
        self.url = video_url
        if title == None:
            self.title = self.yt.title
        else:
            self.title = title
        if author == None:
            self.author = self.yt.author
        else:
            self.author = author
        self.length = self.yt.length
        if playlist == None:
            self.playlist = "None"
        else:
            self.playlist = playlist
        print(f"Video Title: {self.title}")
        print(f"Video Author: {self.author}")
        print(f"Video Length: {self.length} seconds")
        print(f"Video Playlist: {self.playlist}")
        self.add_to_files()
        
    def add_to_files(self):
        # Get only the audio
        audio = self.yt.streams.get_audio_only()
        audio.download('./audios')
        # rename the file
        os.rename("./audios/"+remove_weird_char(self.yt.title)+".mp4", "./audios/"+self.title+".mp4")
        
        with open('index.csv', 'a') as f:
            f.write("\n"+self.title+";"+self.author+";"+self.playlist+";"+self.url+";"+"./audios/"+self.title+".mp4"+";"+str(self.length))

class new_musics_from_yt_playlist:
    def __init__(self, link):
        p = Playlist(link)
        self.p = p
        self.playlist = []
        for video in p.videos:
            self.playlist.append((video.title, video.author, "None", video.watch_url, video.length))
        print("Nombre de vidéos dans la playlist: ", len(p.video_urls))
    
    def get_number_videos(self):
        return len(self.playlist)
    
    def get_name(self):
        return self.p.title
    
    def get_music_info(self, index):
        return self.playlist[index]
    
    def modify_music_info(self, index, title, author, playlist):
        self.playlist[index] = (title, author, playlist, self.playlist[index][3], self.playlist[index][4])
        
    def add_to_files(self):
        for video in self.playlist:
            self._add_one_to_files(video)

    def _add_one_to_files(self, video):
        # Get only the audio
        title, author, playlist, watch_url,length = video
        yt = YouTube(watch_url)
        audio = yt.streams.get_audio_only()
        audio.download('./audios')
        # rename the file
        os.rename("./audios/"+remove_weird_char(yt.title)+".mp4", "./audios/"+title+".mp4")
        
        with open('index.csv', 'a') as f:
            f.write("\n"+title+";"+author+";"+str(playlist)+";"+watch_url+";"+"./audios/"+title+".mp4"+";"+str(length))

class playlist:
    def __init__(self, name):
        print("-- new playlist", name)
       # chercher dans l'index toutes les musiques dans la playlist et les ajouter dans une liste
        self.name = name
        self.musics = []
        with open('index.csv', 'r') as f:
            for line in f:
                if len(line.split(";")) > 2 and line.split(";")[2] == name:
                    self.musics.append(Music(line.split(";")[0], line.split(";")[1], line.split(";")[2], line.split(";")[3], line.split(";")[4], line.split(";")[5]))
        print(self.musics)
    
    def get_one_music(self):
        return  random.choice(self.musics)
    
    def get_length(self):
        return len(self.musics)
        
class full_discography:
    def __init__(self):
        print("-- new full discography")
        self.musics = []
        with open('index.csv', 'r') as f:
            for line in f:
                    self.musics.append(Music(line.split(";")[0], line.split(";")[1], line.split(";")[2], line.split(";")[3], line.split(";")[4], line.split(";")[5]))
        print(self.musics)
    
    def get_one_music(self):
        return  random.choice(self.musics)
    
    def get_length(self):
        return len(self.musics)
        
        
def remove_weird_char(string):
    # remove the char
    string = string.replace("'", "")
    string = string.replace(",", "")
    return string