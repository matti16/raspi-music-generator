import pygame
import os

class Player():

    def __init__(self, folder):
        self.folder = folder
        pygame.init()
    
    def play(self):
        current = 0
        songs = [os.path.join(self.folder, i) for i in sorted(os.listdir(self.folder))]
        pygame.mixer.music.load(songs[current])
        pygame.mixer.music.play()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    
    def stop(self):
        pygame.mixer.music.stop()
        pygame.mmixer.music.unload()

    
