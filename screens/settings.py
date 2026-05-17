import pygame

fonte = pygame.font.SysFont("consolas", 70, bold=True)

def draw_settings(screen):

    screen.fill((20, 15, 55))

    texto = fonte.render("CONFIGURAÇÕES", True, (255,255,255))

    screen.blit(texto, (320, 300))