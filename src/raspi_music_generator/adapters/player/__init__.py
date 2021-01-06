import pygame
import os

class Player():

    def __init__(self, folder):
        self.next_event = pygame.USEREVENT + 1
        self.folder = folder
        pygame.init()
    
    def play(self):
        current = 0
        songs = [os.path.join(self.folder, i) for i in sorted(os.listdir(self.folder))]
        pygame.mixer.music.load(songs[current])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(self.next_event) 

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.next_event:
                    songs = [os.path.join(self.folder, i) for i in sorted(os.listdir(self.folder))]
                    current_track = (current + 1) % len(songs)
                    print("Play:", songs[current_track])
                    pygame.mixer.music.load(songs[current_track])
                    pygame.mixer.music.play()
    
    def stop(self):
        pygame.mixer.music.stop()
        pygame.mmixer.music.unload()

    
