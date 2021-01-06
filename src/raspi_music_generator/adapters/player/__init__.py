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
        pygame.mixer.music.load(self._get_current_song_list()[0])
        pygame.mixer.music.play()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


    def enqueue(self, path):
        pygame.mixer.music.queue(path)


    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    
