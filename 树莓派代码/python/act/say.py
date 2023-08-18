import random
import pygame
pygame.mixer.init()

class voice():
    def play():
        pygame.mixer.music.load('act/cheer/{}.mp3'.format(str(random.randint(1,3))))
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(1)
        while pygame.mixer.music.get_busy():
            pass
        return
def main():
    voice.play()

if __name__ == "__main__":
    main()