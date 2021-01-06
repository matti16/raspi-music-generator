import pygame
import os

class Player():

    def __init__(self, folder):
        self.folder = folder
        self.next = pygame.USEREVENT + 1
        self.songs = [os.path.join(self.folder, i) for i in sorted(os.listdir(self.folder))]
        pygame.init()


    def _refresh_song_list(self):
        self.songs = [os.path.join(self.folder, i) for i in sorted(os.listdir(self.folder))]
    
    
    def play(self):
        current_track = 0
        self._refresh_song_list()
        pygame.mixer.music.load(self.songs[current_track])
        pygame.mixer.music.play()
        print("Play: ", self.songs[current_track])
        pygame.mixer.music.set_endevent(self.next) 

        self._refresh_song_list()
        if len(self.songs) > 1:
            pygame.mixer.music.queue(self.songs[current_track + 1])

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.next:
                    self._refresh_song_list()
                    current_track = (current_track + 1) % len(self.songs)
                    next_track = (current_track + 1) % len(self.songs)
                    pygame.mixer.music.queue(self.songs[next_track])


    def enqueue(self, path):
        pygame.mixer.music.queue(path)

    
    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    
