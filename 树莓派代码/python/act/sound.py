import random
import pygame
pygame.mixer.init()

class voice():
    def play():
        rnd=str(random.randint(1,3))
        pygame.mixer.music.load('act/music/{}.mp3'.format(rnd))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(1)
        while pygame.mixer.music.get_busy():
            pass
        return
def main():
    voice.play()

if __name__ == "__main__":
    main()