import pygame
import sys
import random
import math
from pathlib import Path

pygame.init()

W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("DESAFIO MATEMÁTICO — CÁLCULO GALÁCTICO")
clock = pygame.time.Clock()

BASE_DIR = Path(__file__).resolve().parent.parent
NOME_ARQUIVO_FUNDO = BASE_DIR / "assets" / "images" / "fundodatela.jpeg"

BRANCO = (240, 240, 255)
AZUL_ESCURO = (15, 25, 50)
AZUL_CAIXA = (8, 18, 55)
AZUL_CLARO = (90, 120, 255)
LILAS = (190, 200, 255)
ROXO = AZUL_CLARO
VERMELHO = (255, 80, 100)
VERDE = (80, 255, 160)
CINZA = (180, 190, 220)

fonte_titulo = pygame.font.SysFont("impact", 56)
fonte_grande = pygame.font.SysFont("bahnschrift", 28, bold=True)
fonte_media = pygame.font.SysFont("segoe ui", 22)
fonte_pequena = pygame.font.SysFont("segoe ui", 18)

def carregar_fundo():
    try:
        img = pygame.image.load(str(NOME_ARQUIVO_FUNDO)).convert()
        return pygame.transform.scale(img, (W, H))
    except:
        img = pygame.Surface((W, H))
        for y in range(H):
            r = int(10 + (y / H) * 20)
            g = int(26 + (y / H) * 40)
            b = int(58 + (y / H) * 100)
            pygame.draw.line(img, (r, g, b), (0, y), (W, y))
        return img

def carregar_robo():
    return pygame.Surface((1, 1), pygame.SRCALPHA)

fundo_img = carregar_fundo()
robo_img = carregar_robo()

QUESTOES = [
    {
        "titulo": "PORTAL QUADRÁTICO",
        "texto": "Resolva a equação: x² - 5x + 6 = 0. Digite apenas uma das raízes.",
        "resposta": "2",
        "explicacao": "Fatorando: (x - 2)(x - 3) = 0. As raízes são 2 e 3."
    },
    {
        "titulo": "CÓDIGO DA ESTAÇÃO",
        "texto": "Resolva a equação: x² - 9 = 0. Digite apenas uma raiz positiva.",
        "resposta": "3",
        "explicacao": "x² = 9. x = 3 ou -3. A raiz positiva é 3."
    },
    {
        "titulo": "SISTEMA ORBITAL",
        "texto": "Resolva a equação: x² + 7x + 10 = 0. Digite apenas uma das raízes.",
        "resposta": "-5",
        "explicacao": "Fatorando: (x + 5)(x + 2) = 0. As raízes são -5 e -2."
    },
    {
        "titulo": "REATOR NUMÉRICO",
        "texto": "Resolva a equação: x² - 4x - 12 = 0. Digite apenas uma das raízes.",
        "resposta": "6",
        "explicacao": "Delta = 64. As raízes são 6 e -2."
    },
    {
        "titulo": "ENIGMA GALÁCTICO",
        "texto": "Resolva a equação: x² - 8x + 16 = 0. Digite a raiz.",
        "resposta": "4",
        "explicacao": "(x - 4)² = 0. A raiz é 4."
    }
]

random.shuffle(QUESTOES)

class Estrela:
    def __init__(self):
        self.x = random.randint(0, W)
        self.y = random.randint(0, H)
        self.vel = random.uniform(0.5, 2)
        self.r = random.randint(1, 3)

    def update(self):
        self.x -= self.vel
        if self.x < 0:
            self.x = W
            self.y = random.randint(0, H)

    def draw(self):
        pygame.draw.circle(screen, BRANCO, (int(self.x), int(self.y)), self.r)

estrelas = [Estrela() for _ in range(160)]

def desenhar_texto_wrap(texto, fonte, cor, x, y, largura, max_linhas=None):
    palavras = texto.split(" ")
    linhas = []
    linha = ""

    for palavra in palavras:
        teste = linha + palavra + " "
        if fonte.size(teste)[0] <= largura:
            linha = teste
        else:
            linhas.append(linha.strip())
            linha = palavra + " "

    if linha:
        linhas.append(linha.strip())

    if max_linhas:
        linhas = linhas[:max_linhas]

    for linha in linhas:
        render = fonte.render(linha, True, cor)
        screen.blit(render, (x, y))
        y += fonte.get_height() + 5

def desenhar_botao(rect, texto, mouse):
    hover = rect.collidepoint(mouse)
    cor_fundo = (255, 255, 255, 45) if hover else (255, 255, 255, 20)

    fundo = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(fundo, cor_fundo, fundo.get_rect(), border_radius=15)
    screen.blit(fundo, rect.topleft)

    pygame.draw.rect(screen, AZUL_CLARO, rect, 2, border_radius=15)

    txt = fonte_media.render(texto, True, BRANCO)
    screen.blit(txt, txt.get_rect(center=rect.center))

    return rect

def desenhar_tela_base():
    screen.blit(fundo_img, (0, 0))

    for estrela in estrelas:
        estrela.update()
        estrela.draw()

    overlay = pygame.Surface((W, H))
    overlay.set_alpha(80)
    overlay.fill(AZUL_ESCURO)
    screen.blit(overlay, (0, 0))

def intro():
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                return True

        desenhar_tela_base()

        titulo = fonte_titulo.render("CÁLCULO GALÁCTICO", True, BRANCO)
        screen.blit(titulo, titulo.get_rect(center=(W // 2, 125)))

        pygame.draw.line(screen, AZUL_CLARO, (300, 185), (980, 185), 3)

        sub = fonte_grande.render("Equação do segundo grau — D17", True, LILAS)
        screen.blit(sub, sub.get_rect(center=(W // 2, 225)))

        desenhar_texto_wrap(
            "Aplicar vários métodos para a resolução da equação em diferentes contextos.",
            fonte_media,
            BRANCO,
            260,
            315,
            760
        )

        iniciar = fonte_grande.render("PRESSIONE QUALQUER TECLA", True, VERDE)
        screen.blit(iniciar, iniciar.get_rect(center=(W // 2, 570)))

        pygame.display.flip()

def jogar():
    pontos = 0
    energia = 100

    for pergunta in QUESTOES:
        resposta_digitada = ""
        rascunho = ""
        campo_ativo = "resposta"
        respondido = False
        feedback = ""
        cor_feedback = BRANCO

        while not respondido:
            clock.tick(60)
            mouse = pygame.mouse.get_pos()

            rect_resposta = pygame.Rect(60, 585, 360, 50)
            rect_rascunho = pygame.Rect(700, 170, 470, 360)
            btn_enviar = pygame.Rect(450, 585, 150, 50)
            btn_limpar = pygame.Rect(700, 545, 210, 45)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_resposta.collidepoint(mouse):
                        campo_ativo = "resposta"

                    elif rect_rascunho.collidepoint(mouse):
                        campo_ativo = "rascunho"

                    elif btn_limpar.collidepoint(mouse):
                        rascunho = ""

                    elif btn_enviar.collidepoint(mouse):
                        if resposta_digitada.strip() == pergunta["resposta"]:
                            pontos += 150
                            feedback = "RESPOSTA CORRETA!"
                            cor_feedback = VERDE
                        else:
                            energia -= 35
                            feedback = "RESPOSTA INCORRETA!"
                            cor_feedback = VERMELHO

                        respondido = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        campo_ativo = "rascunho" if campo_ativo == "resposta" else "resposta"

                    elif event.key == pygame.K_BACKSPACE:
                        if campo_ativo == "resposta":
                            resposta_digitada = resposta_digitada[:-1]
                        else:
                            rascunho = rascunho[:-1]

                    elif event.key == pygame.K_RETURN:
                        if campo_ativo == "rascunho":
                            rascunho += "\n"
                        else:
                            if resposta_digitada.strip() == pergunta["resposta"]:
                                pontos += 150
                                feedback = "RESPOSTA CORRETA!"
                                cor_feedback = VERDE
                            else:
                                energia -= 35
                                feedback = "RESPOSTA INCORRETA!"
                                cor_feedback = VERMELHO

                            respondido = True

                    else:
                        if campo_ativo == "resposta":
                            if len(resposta_digitada) < 20:
                                resposta_digitada += event.unicode
                        else:
                            if len(rascunho) < 500:
                                rascunho += event.unicode

            desenhar_tela_base()

            pygame.draw.rect(screen, AZUL_CAIXA, (40, 90, 620, 430), border_radius=12)
            pygame.draw.rect(screen, AZUL_CLARO, (40, 90, 620, 430), 3, border_radius=12)

            titulo = fonte_grande.render(pergunta["titulo"], True, BRANCO)
            screen.blit(titulo, (60, 115))

            desenhar_texto_wrap(pergunta["texto"], fonte_media, BRANCO, 60, 170, 570)

            dica = fonte_pequena.render("Digite a resposta no campo abaixo. Use TAB para alternar campos.", True, CINZA)
            screen.blit(dica, (60, 520))

            cor_borda_resposta = VERDE if campo_ativo == "resposta" else AZUL_CLARO
            pygame.draw.rect(screen, (8, 18, 55), rect_resposta, border_radius=10)
            pygame.draw.rect(screen, cor_borda_resposta, rect_resposta, 2, border_radius=10)

            txt_resp = fonte_media.render(resposta_digitada, True, BRANCO)
            screen.blit(txt_resp, (75, 600))

            desenhar_botao(btn_enviar, "ENVIAR", mouse)

            pygame.draw.rect(screen, AZUL_CAIXA, rect_rascunho, border_radius=12)
            pygame.draw.rect(screen, VERDE if campo_ativo == "rascunho" else AZUL_CLARO, rect_rascunho, 3, border_radius=12)

            titulo_rascunho = fonte_grande.render("RASCUNHO", True, BRANCO)
            screen.blit(titulo_rascunho, (710, 130))

            linhas = rascunho.split("\n")
            y = 190
            for linha in linhas[-11:]:
                txt = fonte_pequena.render(linha, True, BRANCO)
                screen.blit(txt, (720, y))
                y += 28

            desenhar_botao(btn_limpar, "LIMPAR", mouse)

            pygame.draw.rect(screen, (20, 20, 50), (40, 25, 260, 35), border_radius=5)
            pygame.draw.rect(screen, AZUL_CLARO, (40, 25, 260, 35), 2, border_radius=5)
            pygame.draw.rect(screen, VERDE if energia > 40 else VERMELHO, (50, 35, int((energia / 100) * 240), 15), border_radius=3)

            txt_pontos = fonte_media.render(f"PONTOS: {pontos}", True, BRANCO)
            screen.blit(txt_pontos, (1050, 30))

            pygame.display.flip()

        tempo_feedback = pygame.time.get_ticks()

        while pygame.time.get_ticks() - tempo_feedback < 3500:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            desenhar_tela_base()

            titulo = fonte_titulo.render(feedback, True, cor_feedback)
            screen.blit(titulo, titulo.get_rect(center=(W // 2, 130)))

            desenhar_texto_wrap(pergunta["explicacao"], fonte_media, BRANCO, 180, 280, 900)

            pygame.display.flip()

        if energia <= 0:
            break

    fim(pontos, energia)

def fim(pontos, energia):
    venceu = energia > 0

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                return

        desenhar_tela_base()

        msg = "MISSÃO CONCLUÍDA" if venceu else "ENERGIA ESGOTADA"
        cor = VERDE if venceu else VERMELHO

        titulo = fonte_titulo.render(msg, True, cor)
        screen.blit(titulo, titulo.get_rect(center=(W // 2, 140)))

        pts = fonte_grande.render(f"PONTUAÇÃO FINAL: {pontos}", True, BRANCO)
        screen.blit(pts, pts.get_rect(center=(W // 2, 280)))

        sair = fonte_media.render("PRESSIONE QUALQUER TECLA PARA VOLTAR", True, CINZA)
        screen.blit(sair, sair.get_rect(center=(W // 2, 620)))

        pygame.display.flip()

def executar_jogo():
    if intro():
        jogar()

if __name__ == "__main__":
    executar_jogo()
    pygame.quit()
    sys.exit()