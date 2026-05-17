import pygame

pygame.font.init()

fonte_titulo = pygame.font.SysFont("consolas", 55, bold=True)
fonte_card = pygame.font.SysFont("consolas", 30, bold=True)
fonte_botao = pygame.font.SysFont("consolas", 24, bold=True)
fonte_pequena = pygame.font.SysFont("consolas", 20, bold=True)

def draw_card(screen, x, y, titulo, serie, cor):
    card = pygame.Rect(x, y, 280, 310)

    pygame.draw.rect(screen, (5, 20, 65), card, border_radius=18)
    pygame.draw.rect(screen, (40, 180, 255), card, 4, border_radius=18)

    pygame.draw.circle(screen, cor, (x + 140, y + 80), 45)
    pygame.draw.circle(screen, (255, 255, 255), (x + 140, y + 80), 45, 3)

    texto = fonte_card.render(titulo, True, (255, 255, 255))
    screen.blit(texto, (x + 140 - texto.get_width() // 2, y + 145))

    texto_serie = fonte_pequena.render(serie, True, (90, 210, 255))
    screen.blit(texto_serie, (x + 140 - texto_serie.get_width() // 2, y + 185))

    botao = pygame.Rect(x + 55, y + 225, 170, 55)
    pygame.draw.rect(screen, (0, 120, 255), botao, border_radius=12)
    pygame.draw.rect(screen, (100, 220, 255), botao, 3, border_radius=12)

    start = fonte_botao.render("START", True, (255, 255, 255))
    screen.blit(start, (botao.centerx - start.get_width() // 2, botao.centery - start.get_height() // 2))

    return botao

def draw_game(screen):
    screen.fill((4, 10, 35))

    pygame.draw.rect(screen, (0, 70, 180), (35, 35, 1295, 690), 3, border_radius=10)

    titulo = fonte_titulo.render("SELECIONE UMA MATÉRIA", True, (255, 255, 255))
    screen.blit(titulo, (90, 60))

    config = pygame.Rect(1190, 55, 80, 60)
    pygame.draw.rect(screen, (0, 100, 220), config, border_radius=10)
    pygame.draw.rect(screen, (80, 210, 255), config, 3, border_radius=10)

    engrenagem = fonte_card.render("⚙", True, (255, 255, 255))
    screen.blit(engrenagem, (config.centerx - engrenagem.get_width() // 2, config.centery - engrenagem.get_height() // 2))

    portugues = draw_card(screen, 150, 210, "PORTUGUÊS", "3º - 12º", (80, 170, 255))
    matematica = draw_card(screen, 540, 210, "MATEMÁTICA", "1º - 12º", (255, 190, 50))
    biologia = draw_card(screen, 930, 210, "BIOLOGIA", "1º - 11º", (80, 220, 120))

    voltar = pygame.Rect(60, 650, 180, 50)
    pygame.draw.rect(screen, (0, 80, 180), voltar, border_radius=10)
    texto_voltar = fonte_botao.render("ESC VOLTAR", True, (255, 255, 255))
    screen.blit(texto_voltar, (voltar.centerx - texto_voltar.get_width() // 2, voltar.centery - texto_voltar.get_height() // 2))

    return portugues, matematica, biologia, config