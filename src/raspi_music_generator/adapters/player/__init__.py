import pygame
import os

class Player():

    def __init__(self, folder):
        self.folder = folder
        pygame.init()
        pygame.mixer.init()


    def _get_current_song_list(self):
        return [os.path.join(self.folder, i) for i in sorted(os.listdir(self.folder))]
    
    
    def play(self):
        self.played_songs = set()
        current_songs = self._get_current_song_list()

        pygame.mixer.music.load(current_songs[0])
        pygame.mixer.music.play()
        self.played_songs.add(current_songs[0])
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT:
                    current_songs = self._get_current_song_list()
                    songs_left = [c for c in current_songs if c not in self.played_songs]
                    if len(songs_left):
                        self.enqueue(songs_left[0])


    def enqueue(self, path):
        pygame.mixer.music.queue(path)
        self.played_songs.add(path)
    
    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    
