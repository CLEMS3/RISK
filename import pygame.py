import pygame
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"



def main():
    pygame.init()

    
    screen = pygame.display.set_mode((480, 320))
    #premier triangle
    button1 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('156137.png').convert_alpha(), (100, 100)), 180)

    button_pos1 = (100, 100)
    mask1 = pygame.mask.from_surface(button1)

    #deuxième triangle
    button2 = pygame.transform.scale(pygame.image.load('156137.png').convert_alpha(), (100, 100))
    button_pos2 = (150, 100)
    mask2 = pygame.mask.from_surface(button2)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                try:
                    if mask1.get_at((e.pos[0]-button_pos1[0], e.pos[1]-button_pos1[1])):
                        print("bouton 1")

                    if mask2.get_at((e.pos[0]-button_pos2[0], e.pos[1]-button_pos2[1])):
                        print("bouton 2")
                    
                except IndexError:
                    pass

        screen.fill((80,80,80))
        
        screen.blit(button2, button_pos2)
        screen.blit(button1, button_pos1)
        pygame.display.flip()

main()