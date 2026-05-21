
import pygame
import sys
import random
import math

# ======================================================
# ROBÔ DETECTOR — D1 INFERÊNCIA IMPLÍCITA (SAEB/SAESE)
# ======================================================

pygame.init()

# CONFIGURAÇÃO DO ARQUIVO DE IMAGEM EXTERNO
NOME_ARQUIVO_FUNDO = "FUNDODATELA.PNG"

def carregar_fundo_customizado():
    """Tenta carregar a imagem que você colocou na pasta. Se não achar, usa um fundo reserva."""
    try:
        img = pygame.image.load(NOME_ARQUIVO_FUNDO)
        return img
    except Exception as e:
        print(f"Aviso: Não foi possível carregar '{NOME_ARQUIVO_FUNDO}'. Usando fundo padrão. Erro: {e}")
        img = pygame.Surface((1280, 720))
        for y in range(720):
            r = int(10 + (y / 720) * 20)
            g = int(26 + (y / 720) * 40)
            b = int(58 + (y / 720) * 100)
            pygame.draw.line(img, (r, g, b), (0, y), (1280, y))
        return img

def criar_png_robo():
    """Tenta carregar o PNG do robô da pasta correta ou desenha um reserva pequeno"""
    try:
        img = pygame.image.load("boss/hehe.PNG")
        return img
    except:
        # Robô reserva corrigido (Sem o bloco azul gigante esticado)
        img = pygame.Surface((180, 180), pygame.SRCALPHA)
        pygame.draw.rect(img, (0, 150, 255, 220), (10, 10, 160, 160), border_radius=15)
        pygame.draw.rect(img, (0, 255, 255, 255), (10, 10, 160, 160), 3, border_radius=15)
        # Olhos
        pygame.draw.circle(img, (255, 255, 255), (60, 70), 12)
        pygame.draw.circle(img, (255, 255, 255), (120, 70), 12)
        pygame.draw.circle(img, (0, 0, 0), (60, 70), 5)
        pygame.draw.circle(img, (0, 0, 0), (120, 70), 5)
        # Boca
        pygame.draw.line(img, (0, 0, 0), (55, 120), (125, 120), 4)
        return img

# Inicializa imagens e escala
fundo_img = carregar_fundo_customizado()
fundo_img = pygame.transform.scale(fundo_img, (1280, 720))
robo_img = criar_png_robo()

# ======================================================
# CONFIGURAÇÕES CUSTOMIZÁVEIS
# ======================================================
W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("ROBÔ DETECTOR — Inferência Galáctica")
clock = pygame.time.Clock()

# Posição e escala perfeita do robô na tela
ROBO_X = 960 
ROBO_Y = 120   
ROBO_LARGURA = 180  
ROBO_ALTURA = 180   

COR_TITULO_PROBLEMA = (75, 0, 130)      
COR_TITULO_SECOES = (106, 90, 205)          
COR_TEXTO_PRINCIPAL = (255, 255, 255)     
COR_OPCOES = (240, 245, 255)              
COR_DICA = (255, 255, 255)                

COR_FUNDO_CAIXAS = (20, 35, 60)           
COR_BORDA_PROBLEMA = (75, 0, 130)         
COR_BORDA_PISTAS = (75, 0, 130)         
COR_BORDA_OPCOES = (75, 0, 130)         
COR_BORDA_OPCOES_HOVER = (106, 90, 205)    
COR_FUNDO_OPCOES_HOVER = (35, 50, 90)     

COR_FUNDO_BARRA = (20, 20, 50)            
COR_BORDA_BARRA = (200, 100, 255)         
COR_BARRA_VIVA = (106, 90, 205)           
COR_BARRA_BAIXA = (255, 80, 100)          

COR_TEXTO_BARRA = (240, 245, 255)        
COR_PONTOS = (255, 255, 255)          

AZUL_ESCURO = (15, 25, 50)
CIANO = (75, 0, 130)
VERDE_NEON = (106, 90, 205)   
VERMELHO_NEON = (255, 80, 100)
AMARELO_NEON = (106, 90, 205)   
BRANCO = (240, 245, 255)
CINZA_CLARO = (180, 190, 200)

fonte_titulo = pygame.font.SysFont("consolas", 42, bold=True)
fonte_media = pygame.font.SysFont("consolas", 20)
fonte_pequena = pygame.font.SysFont("consolas", 16)
fonte_grande = pygame.font.SysFont("consolas", 26, bold=True)

# ------------------------------------------------------
# QUESTÕES NÍVEL SAEB/SAESE
# ------------------------------------------------------
QUESTOES = [
    {
        "titulo": "ESTAÇÃO ORBITAL KRONOS",
        "texto": "Os cientistas da estação Kronos suspenderam a missão de coleta apenas duas horas antes da partida. Embora os relatórios oficiais afirmassem que os motores estavam em perfeito funcionamento, os engenheiros foram vistos deixando o setor principal em silêncio e carregando equipamentos de emergência.",
        "pistas": ["Relatórios afirmavam que tudo estava normal.", "Engenheiros carregavam equipamentos de emergência.", "A missão foi cancelada pouco antes da partida."],
        "opcoes": ["A missão foi cancelada por falta de combustível.", "Os engenheiros desconfiavam de um possível risco oculto.", "Os motores haviam sido destruídos publicamente.", "Os cientistas decidiram cancelar a missão sem motivo."],
        "correta": 1,
        "explicacao": "Mesmo com relatórios positivos, o comportamento dos engenheiros sugere que havia um risco não revelado oficialmente."
    },
    {
        "titulo": "COLÔNIA DE TITÃ",
        "texto": "Durante semanas, os moradores da colônia afirmaram que as luzes da torre central apagavam exatamente no mesmo horário. Ainda assim, o diretor da base insistia em dizer que o sistema elétrico jamais apresentou falhas. Na noite anterior à auditoria, a torre permaneceu completamente iluminada pela primeira vez no mês.",
        "pistas": ["As falhas sempre aconteciam no mesmo horário.", "O diretor negava qualquer problema.", "Antes da auditoria, o problema desapareceu."],
        "opcoes": ["O problema provavelmente era conhecido pela direção.", "As luzes apagavam por causa do clima espacial.", "Os moradores inventaram as falhas da torre.", "A auditoria causou pane elétrica na base."],
        "correta": 0,
        "explicacao": "O desaparecimento das falhas justamente antes da auditoria sugere tentativa de ocultar o problema."
    },
    {
        "titulo": "SINAL DE ORION",
        "texto": "A equipe de comunicação afirmou que o sinal vindo de Orion era apenas interferência comum. No entanto, horas depois, os mesmos pesquisadores passaram a utilizar códigos criptografados e restringiram o acesso aos arquivos da transmissão.",
        "pistas": ["O sinal foi chamado de simples interferência.", "Depois disso, os arquivos foram restringidos.", "A equipe passou a usar criptografia."],
        "opcoes": ["Os cientistas consideraram o sinal irrelevante.", "Os pesquisadores acreditavam que havia algo importante no sinal.", "A transmissão destruiu os computadores da estação.", "A equipe decidiu abandonar completamente as pesquisas."],
        "correta": 1,
        "explicacao": "O comportamento da equipe sugere que o sinal continha informações relevantes ou perigosas."
    }
]

random.shuffle(QUESTOES)

# ------------------------------------------------------
# ESTRELAS
# ------------------------------------------------------
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

estrelas = [Estrela() for _ in range(180)]

# ------------------------------------------------------
# PARTÍCULAS
# ------------------------------------------------------
class Particula:
    def __init__(self, x, y, cor):
        ang = random.uniform(0, math.pi * 2)
        vel = random.uniform(2, 8)
        self.x = x
        self.y = y
        self.vx = math.cos(ang) * vel
        self.vy = math.sin(ang) * vel
        self.vida = 1
        self.cor = cor

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 0.03

    def draw(self):
        if self.vida > 0:
            pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), 4)

particulas = []

def explodir(x, y, cor):
    for _ in range(40):
        particulas.append(Particula(x, y, cor))

def desenhar_robo(x, y, estado="normal"):
    robo_redimensionado = pygame.transform.scale(robo_img, (ROBO_LARGURA, ROBO_ALTURA))
    screen.blit(robo_redimensionado, (x, y))

def desenhar_texto_com_wrap(texto, fonte, cor, x, y, largura, altura=None, max_linhas=None):
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        teste = linha_atual + palavra + " "
        if fonte.size(teste)[0] <= largura:
            linha_atual = teste
        else:
            if linha_atual:
                linhas.append(linha_atual.strip())
            linha_atual = palavra + " "
    if linha_atual:
        linhas.append(linha_atual.strip())

    if max_linhas:
        linhas = linhas[:max_linhas]

    y_offset = y
    for linha in linhas:
        if altura and y_offset - y > altura:
            break
        render = fonte.render(linha, True, cor)
        screen.blit(render, (x, y_offset))
        y_offset += fonte.get_height() + 4

# ------------------------------------------------------
# INTRO
# ------------------------------------------------------
def intro():
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        screen.blit(fundo_img, (0, 0))

        for estrela in estrelas:
            estrela.update()
            estrela.draw()

        overlay = pygame.Surface((W, H))
        overlay.set_alpha(80)
        overlay.fill(AZUL_ESCURO)
        screen.blit(overlay, (0, 0))

        titulo = fonte_titulo.render("ROBÔ DETECTOR", True, CIANO)
        subtitulo = fonte_grande.render("INFERÊNCIA IMPLÍCITA — D1", True, AMARELO_NEON)

        screen.blit(titulo, (W//2 - titulo.get_width()//2, 120))
        screen.blit(subtitulo, (W//2 - subtitulo.get_width()//2, 190))

        desenhar_texto_com_wrap(
            "Analise pistas ocultas, descubra contradições e detecte informações implícitas nas transmissões galácticas.",
            fonte_media,
            BRANCO,
            240,
            300,
            800
        )

        iniciar = fonte_grande.render("PRESSIONE QUALQUER TECLA", True, VERDE_NEON)
        screen.blit(iniciar, (W//2 - iniciar.get_width()//2, 560))

        desenhar_robo(ROBO_X, ROBO_Y)
        pygame.display.flip()

def scanner_animado(fase):
    linha_y = 100 + (fase % 450)
    pygame.draw.line(screen, VERDE_NEON, (40, linha_y), (1000, linha_y), 2)

# ------------------------------------------------------
# JOGO
# ------------------------------------------------------
def jogar():
    pontos = 0
    energia = 100
    estado_robo = "normal"

    for pergunta in QUESTOES:
        escolha = None
        respondido = False
        fase = 0

        while not respondido:
            clock.tick(60)
            fase += 3

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: escolha = 0
                    elif event.key == pygame.K_2: escolha = 1
                    elif event.key == pygame.K_3: escolha = 2
                    elif event.key == pygame.K_4: escolha = 3

                    if escolha is not None:
                        respondido = True
                        if escolha == pergunta["correta"]:
                            pontos += 150
                            estado_robo = "feliz"
                            explodir(W//2, H//2, VERDE_NEON)
                        else:
                            energia -= 35
                            estado_robo = "triste"
                            explodir(W//2, H//2, VERMELHO_NEON)

            screen.blit(fundo_img, (0, 0))

            for estrela in estrelas:
                estrela.update()
                estrela.draw()

            desenhar_robo(ROBO_X, ROBO_Y, estado_robo)

            overlay_jogo = pygame.Surface((W, H))
            overlay_jogo.set_alpha(80)
            overlay_jogo.fill(AZUL_ESCURO)
            screen.blit(overlay_jogo, (0, 0))

            scanner_animado(fase)

            # HUD
            pygame.draw.rect(screen, COR_FUNDO_BARRA, (20, 20, 260, 40), border_radius=5)
            pygame.draw.rect(screen, COR_BORDA_BARRA, (20, 20, 260, 40), 2, border_radius=5)
            barra = int((energia / 100) * 240)
            cor_barra = COR_BARRA_VIVA if energia > 40 else COR_BARRA_BAIXA
            pygame.draw.rect(screen, cor_barra, (30, 30, barra, 20), border_radius=3)

            txt_energia = fonte_pequena.render("ESTABILIDADE NEURAL", True, COR_TEXTO_BARRA)
            screen.blit(txt_energia, (35, 4))

            txt_pontos = fonte_media.render(f"PONTOS: {pontos}", True, COR_PONTOS)
            screen.blit(txt_pontos, (1050, 25))

            # CAIXA DO PROBLEMA
            pygame.draw.rect(screen, COR_FUNDO_CAIXAS, (40, 90, 900, 220), border_radius=10)
            pygame.draw.rect(screen, COR_BORDA_PROBLEMA, (40, 90, 900, 220), 3, border_radius=10)
            titulo = fonte_grande.render(pergunta["titulo"], True, COR_TITULO_PROBLEMA)
            screen.blit(titulo, (60, 105))

            desenhar_texto_com_wrap(pergunta["texto"], fonte_pequena, COR_TEXTO_PRINCIPAL, 60, 160, 860, altura=140)

            # PISTAS
            pistas_titulo = fonte_grande.render("PISTAS DETECTADAS", True, COR_TITULO_SECOES)
            screen.blit(pistas_titulo, (40, 340))
            for i, pista in enumerate(pergunta["pistas"]):
                y_pos = 390 + i*55
                pygame.draw.rect(screen, COR_FUNDO_CAIXAS, (60, y_pos, 540, 50), border_radius=8)
                pygame.draw.rect(screen, COR_BORDA_PISTAS, (60, y_pos, 540, 50), 2, border_radius=8)
                desenhar_texto_com_wrap("• " + pista, fonte_pequena, COR_TEXTO_PRINCIPAL, 75, y_pos + 7, 500, max_linhas=2)

            # OPÇÕES
            op_titulo = fonte_grande.render("CONCLUSÃO MAIS PROVÁVEL", True, COR_TITULO_SECOES)
            screen.blit(op_titulo, (650, 340))
            for i, opcao in enumerate(pergunta["opcoes"]):
                mx, my = pygame.mouse.get_pos()
                rect = pygame.Rect(670, 390 + i*60, 520, 55)
                hover = rect.collidepoint(mx, my)
                cor_fundo = COR_FUNDO_OPCOES_HOVER if hover else COR_FUNDO_CAIXAS
                cor_borda = COR_BORDA_OPCOES_HOVER if hover else COR_BORDA_OPCOES
                pygame.draw.rect(screen, cor_fundo, rect, border_radius=8)
                pygame.draw.rect(screen, cor_borda, rect, 2, border_radius=8)
                desenhar_texto_com_wrap(f"[{i+1}] {opcao}", fonte_pequena, COR_OPCOES, 685, rect.y + 7, 490, max_linhas=2)

            dica = fonte_pequena.render("PRESSIONE 1, 2, 3 OU 4", True, COR_DICA)
            screen.blit(dica, (890, 675))

            for p in particulas[:]:
                p.update()
                p.draw()
                if p.vida <= 0: particulas.remove(p)

            pygame.display.flip()

        # FEEDBACK
        tempo_feedback = pygame.time.get_ticks()
        while pygame.time.get_ticks() - tempo_feedback < 3500:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(fundo_img, (0, 0))
            for estrela in estrelas:
                estrela.update()
                estrela.draw()

            desenhar_robo(ROBO_X, ROBO_Y, estado_robo)

            overlay = pygame.Surface((W, H))
            overlay.set_alpha(100)
            overlay.fill(AZUL_ESCURO)
            screen.blit(overlay, (0, 0))

            acertou = escolha == pergunta["correta"]
            msg = "INFERÊNCIA CORRETA" if acertou else "ANÁLISE INCONSISTENTE"
            cor = VERDE_NEON if acertou else VERMELHO_NEON
            titulo = fonte_titulo.render(msg, True, cor)
            screen.blit(titulo, (W//2 - titulo.get_width()//2, 120))

            desenhar_texto_com_wrap(pergunta["explicacao"], fonte_media, BRANCO, 180, 280, 900)
            pygame.display.flip()

        estado_robo = "normal"
        if energia <= 0: break

    fim(pontos, energia)

# ------------------------------------------------------
# FINAL
# ------------------------------------------------------
def fim(pontos, energia):
    venceu = energia > 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(fundo_img, (0, 0))
        for estrela in estrelas:
            estrela.update()
            estrela.draw()

        desenhar_robo(ROBO_X, ROBO_Y, "feliz" if venceu else "triste")

        overlay = pygame.Surface((W, H))
        overlay.set_alpha(100)
        overlay.fill(AZUL_ESCURO)
        screen.blit(overlay, (0, 0))

        msg = "MISSÃO CONCLUÍDA" if venceu else "COLAPSO NEURAL"
        cor = VERDE_NEON if venceu else VERMELHO_NEON
        titulo = fonte_titulo.render(msg, True, cor)
        screen.blit(titulo, (W//2 - titulo.get_width()//2, 120))

        pts = fonte_grande.render(f"PONTUAÇÃO FINAL: {pontos}", True, COR_PONTOS)
        screen.blit(pts, (W//2 - pts.get_width()//2, 260))

        if pontos >= 400: rank = "ANALISTA DE INFERÊNCIA NÍVEL ÔMEGA"
        elif pontos >= 250: rank = "INVESTIGADOR AVANÇADO"
        else: rank = "RECRUTA INTERPRETATIVO"

        txt_rank = fonte_grande.render(rank, True, CIANO)
        screen.blit(txt_rank, (W//2 - txt_rank.get_width()//2, 340))

        sair = fonte_media.render("FECHE A JANELA PARA ENCERRAR", True, CINZA_CLARO)
        screen.blit(sair, (W//2 - sair.get_width()//2, 650))

        pygame.display.flip()

if __name__ == "__main__":
    intro()
    jogar()
    pygame.quit()
    sys.exit()
