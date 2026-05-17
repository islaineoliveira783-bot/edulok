import pygame
import sys
import random

pygame.init()

LARGURA, ALTURA = 1000, 560
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tela de Matérias")

clock = pygame.time.Clock()

AZUL_ESCURO = (3, 10, 35)
AZUL_NEON = (35, 210, 255)
AZUL_BOTAO = (5, 65, 130)
BRANCO = (245, 248, 255)
CINZA = (150, 160, 175)
CINZA_CLARO = (205, 210, 220)
TEXTO = (20, 30, 55)
TEXTO_CLARO = (235, 245, 255)

fonte_titulo = pygame.font.SysFont("arial", 32, bold=True)
fonte_media = pygame.font.SysFont("arial", 24, bold=True)
fonte_pequena = pygame.font.SysFont("arial", 18, bold=True)
fonte_mini = pygame.font.SysFont("arial", 14, bold=True)

robo_img = pygame.image.load("assets/images/robo.png.png").convert_alpha()

largura_original = robo_img.get_width()
altura_original = robo_img.get_height()

nova_altura = 380
nova_largura = int(largura_original * (nova_altura / altura_original))

robo_img = pygame.transform.scale(robo_img, (nova_largura, nova_altura))

estrelas = []
for i in range(120):
    estrelas.append([
        random.randint(0, LARGURA),
        random.randint(0, ALTURA),
        random.uniform(0.3, 1.4),
        random.randint(1, 2)
    ])

# Retângulos dos botões
botao_editar_rect = pygame.Rect(0, 0, 0, 0)
botao_portugues_rect = pygame.Rect(0, 0, 0, 0)
botao_matematica_rect = pygame.Rect(0, 0, 0, 0)
botao_biologia_rect = pygame.Rect(0, 0, 0, 0)


def escrever(txt, x, y, cor, fonte):
    img = fonte.render(txt, True, cor)
    rect = img.get_rect(center=(x, y))
    tela.blit(img, rect)


def fundo_animado():
    tela.fill(AZUL_ESCURO)

    for estrela in estrelas:
        estrela[1] += estrela[2]

        if estrela[1] > ALTURA:
            estrela[0] = random.randint(0, LARGURA)
            estrela[1] = 0

        pygame.draw.circle(
            tela,
            (60, 190, 255),
            (int(estrela[0]), int(estrela[1])),
            estrela[3]
        )


def perfil_player(x, y):
    global botao_editar_rect

    largura = 245
    altura = 105

    painel = pygame.Surface((largura, altura), pygame.SRCALPHA)

    pygame.draw.rect(
        painel,
        (5, 25, 65, 190),
        (0, 0, largura, altura),
        border_radius=18
    )

    tela.blit(painel, (x, y))

    pygame.draw.rect(
        tela,
        AZUL_NEON,
        (x, y, largura, altura),
        2,
        border_radius=18
    )

    # ícone do perfil
    pygame.draw.circle(tela, AZUL_NEON, (x + 43, y + 39), 25, 2)
    pygame.draw.circle(tela, AZUL_NEON, (x + 43, y + 30), 8)
    pygame.draw.arc(tela, AZUL_NEON, (x + 24, y + 40, 38, 28), 3.14, 0, 3)

    escrever("ISLAINE", x + 125, y + 24, TEXTO_CLARO, fonte_pequena)
    escrever("Nível 12", x + 118, y + 50, TEXTO_CLARO, fonte_mini)
    escrever("Português: 3-12", x + 132, y + 70, TEXTO_CLARO, fonte_mini)

    # barra de XP
    pygame.draw.line(
        tela,
        CINZA_CLARO,
        (x + 80, y + 90),
        (x + 175, y + 90),
        6
    )

    pygame.draw.line(
        tela,
        AZUL_NEON,
        (x + 80, y + 90),
        (x + 150, y + 90),
        6
    )

    escrever("XP", x + 195, y + 90, TEXTO_CLARO, fonte_mini)

    # botão editar personagem
    botao_editar_rect = pygame.Rect(x + 200, y + 15, 32, 32)

    pygame.draw.rect(
        tela,
        AZUL_BOTAO,
        botao_editar_rect,
        border_radius=9
    )

    pygame.draw.rect(
        tela,
        AZUL_NEON,
        botao_editar_rect,
        2,
        border_radius=9
    )

    escrever("✎", x + 216, y + 31, BRANCO, fonte_pequena)


def card(x, y, materia, nivel, bloqueado=False):
    largura = 210
    altura = 320

    sombra = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(
        sombra,
        (0, 0, 0, 90),
        (8, 8, largura - 8, altura - 8),
        border_radius=10
    )
    tela.blit(sombra, (x, y))

    # card azul transparente
    card_surface = pygame.Surface((largura, altura), pygame.SRCALPHA)

    pygame.draw.rect(
        card_surface,
        (170, 220, 255, 165),
        (0, 0, largura, altura),
        border_radius=10
    )

    tela.blit(card_surface, (x, y))

    pygame.draw.rect(
        tela,
        AZUL_NEON,
        (x, y, largura, altura),
        2,
        border_radius=10
    )

    escrever(nivel, x + largura // 2, y + 35, TEXTO, fonte_media)

    pygame.draw.line(tela, CINZA_CLARO, (x + 25, y + 70), (x + 185, y + 70), 6)
    pygame.draw.line(tela, AZUL_BOTAO, (x + 25, y + 70), (x + 115, y + 70), 6)

    escrever(materia, x + largura // 2, y + 135, TEXTO, fonte_titulo)

    pygame.draw.line(tela, AZUL_BOTAO, (x + 25, y + 230), (x + 185, y + 230), 3)

    if bloqueado:
        cor_botao = (135, 145, 160)
        texto_botao = "BLOQUEADO"
    else:
        cor_botao = AZUL_BOTAO
        texto_botao = "COMEÇAR"

    botao_rect = pygame.Rect(x + 30, y + 255, 150, 55)

    pygame.draw.rect(
        tela,
        cor_botao,
        botao_rect,
        border_radius=25
    )

    pygame.draw.rect(
        tela,
        AZUL_NEON if not bloqueado else CINZA,
        botao_rect,
        2,
        border_radius=25
    )

    escrever(texto_botao, x + largura // 2, y + 283, BRANCO, fonte_pequena)

    return botao_rect


def painel_robo(x, y):
    largura = 190
    altura = 420

    pygame.draw.rect(tela, (5, 25, 65), (x, y, largura, altura), border_radius=20)
    pygame.draw.rect(tela, AZUL_NEON, (x, y, largura, altura), 2, border_radius=20)

    robo_x = x + (largura - robo_img.get_width()) // 2
    robo_y = y + 20

    tela.blit(robo_img, (robo_x, robo_y))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if botao_editar_rect.collidepoint(mouse_pos):
                print("Abrir tela para editar personagem")

            if botao_portugues_rect.collidepoint(mouse_pos):
                print("Começar Português")

            if botao_matematica_rect.collidepoint(mouse_pos):
                print("Matemática bloqueada")

            if botao_biologia_rect.collidepoint(mouse_pos):
                print("Biologia bloqueada")

    fundo_animado()

    perfil_player(20, 15)

    painel_robo(35, 125)

    botao_portugues_rect = card(270, 150, "Português", "1-12", False)
    botao_matematica_rect = card(510, 150, "Matemática", "1-12", True)
    botao_biologia_rect = card(750, 150, "Biologia", "1-12", True)

    pygame.display.flip()
    clock.tick(60)