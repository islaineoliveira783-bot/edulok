import pygame
from sys import exit

pygame.init()

# ══════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ══════════════════════════════════════════════════════

largura = 1280
altura = 720

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Edulock")

relogio = pygame.time.Clock()

# ══════════════════════════════════════════════════════
# CORES
# ══════════════════════════════════════════════════════

FUNDO = (8, 12, 30)

AZUL = (45, 70, 180)
AZUL_CLARO = (90, 120, 255)

BRANCO = (240, 240, 255)

# ══════════════════════════════════════════════════════
# FONTES
# ══════════════════════════════════════════════════════

fonte_titulo = pygame.font.SysFont("impact", 70)
fonte_card = pygame.font.SysFont("impact", 32)

# ══════════════════════════════════════════════════════
# FUNDO
# ══════════════════════════════════════════════════════

img_fundo = pygame.image.load(
    "assets/images/fundodatela.jpeg"
).convert()

img_fundo = pygame.transform.scale(
    img_fundo,
    (largura, altura)
)

# ══════════════════════════════════════════════════════
# IMAGEM DO ROBÔ
# ══════════════════════════════════════════════════════

img_robo = pygame.image.load(
    "assets/images/robo.png"
).convert_alpha()

img_robo = pygame.transform.smoothscale(
    img_robo,
    (220, 260)
)


# ══════════════════════════════════════════════════════
# FUNÇÃO CARD
# ══════════════════════════════════════════════════════

def desenhar_card(
    x,
    y,
    largura_card,
    altura_card,
    texto,
    mouse,
    imagem=None,
    emoji=None
):

    rect = pygame.Rect(x, y, largura_card, altura_card)

    hover = rect.collidepoint(mouse)

    escala = 1.04 if hover else 1

    nova_largura = int(largura_card * escala)
    nova_altura = int(altura_card * escala)

    x = x - (nova_largura - largura_card)//2
    y = y - (nova_altura - altura_card)//2

    rect_anim = pygame.Rect(
        x,
        y,
        nova_largura,
        nova_altura
    )

    # brilho
    glow = pygame.Surface(
        (nova_largura + 20, nova_altura + 20),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        glow,
        (80, 120, 255, 90),
        glow.get_rect(),
        border_radius=25
    )

    tela.blit(glow, (x - 10, y - 10))

    # fundo do card
    fundo = pygame.Surface(
        (nova_largura, nova_altura),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        fundo,
        (15, 20, 50, 220),
        fundo.get_rect(),
        border_radius=25
    )

    tela.blit(fundo, (x, y))

    # borda
    pygame.draw.rect(
        tela,
        AZUL_CLARO if hover else AZUL,
        rect_anim,
        3,
        border_radius=25
    )

    # imagem
    if imagem:

        img_rect = imagem.get_rect(
            center=(x + nova_largura//2, y + 120)
        )

        tela.blit(imagem, img_rect)

    # emoji
    elif emoji:

        fonte_emoji = pygame.font.SysFont(
            "Segoe UI Emoji",
            70
        )

        emoji_surf = fonte_emoji.render(
            emoji,
            True,
            BRANCO
        )

        tela.blit(
            emoji_surf,
            emoji_surf.get_rect(
                center=(x + nova_largura//2, y + 110)
            )
        )

    # texto
    txt = fonte_card.render(
        texto,
        True,
        BRANCO
    )

    tela.blit(
        txt,
        txt.get_rect(
            center=(
                x + nova_largura//2,
                y + nova_altura - 40
            )
        )
    )

# ══════════════════════════════════════════════════════
# LOOP
# ══════════════════════════════════════════════════════

while True:

    mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    # fundo
    tela.blit(img_fundo, (0, 0))

    # ══════════════════════════════════════════════════
    # TÍTULO
    # ══════════════════════════════════════════════════

    titulo = fonte_titulo.render(
        "ESCOLHA SUA MISSÃO",
        True,
        BRANCO
    )

    tela.blit(
        titulo,
        titulo.get_rect(
            center=(largura//2, 100)
        )
    )

    # linha decorativa
    pygame.draw.line(
        tela,
        AZUL_CLARO,
        (300, 160),
        (980, 160),
        3
    )

    # ══════════════════════════════════════════════════
    # CARDS
    # ══════════════════════════════════════════════════

    largura_card = 240
    altura_card = 320

    espaco = 30

    total = (largura_card * 4) + (espaco * 3)

    inicio_x = (largura - total) // 2

    y = 220

 # ROBÔ GRANDE NA ESQUERDA
desenhar_card(
    80,
    210,
    260,
    420,
    "ROBÔ",
    mouse,
    imagem=img_robo
)

# PORTUGUÊS
desenhar_card(
    390,
    260,
    230,
    300,
    "PORTUGUÊS",
    mouse,
    emoji="📘"
)

# MATEMÁTICA
desenhar_card(
    660,
    260,
    230,
    300,
    "MATEMÁTICA",
    mouse,
    emoji="🔢"
)

# MONITOR
desenhar_card(
    930,
    260,
    230,
    300,
    "MONITOR",
    mouse,
    emoji="🧑‍🏫"
)

pygame.display.update()

relogio.tick(60)