import pygame

pygame.font.init()

background = pygame.image.load("assets/images/fundoo.jpeg")
background = pygame.transform.scale(background, (1365, 768))

def draw_menu(screen):
    screen.blit(background, (0, 0))

    iniciar = pygame.Rect(310, 285, 430, 85)
    config = pygame.Rect(310, 405, 430, 85)
    sair = pygame.Rect(310, 525, 430, 85)

    return iniciar, config, sair