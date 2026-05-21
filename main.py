import pygame
from sys import exit
import random
import math
import subprocess

pygame.init()

LARGURA = 1280
ALTURA = 720

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Edulock")
relogio = pygame.time.Clock()

AZUL_CLARO = (90, 120, 255)
BRANCO = (240, 240, 255)

MENU = "menu"
PORTUGUES = "portugues"
MATEMATICA = "matematica"
AUXILIADOR = "auxiliador"
CHAT = "chat"

estado = MENU
serie_escolhida = None

scroll_y = 0
arrastando = False
mouse_y_anterior = 0

monitor_atual = ""
mensagens_chat = []
texto_digitado = ""
tempo_resposta = None

fonte_titulo = pygame.font.SysFont("impact", 70)
fonte_card = pygame.font.SysFont("bahnschrift", 22, bold=True)
fonte_botao = pygame.font.SysFont("bahnschrift", 24, bold=True)
fonte_sub = pygame.font.SysFont("segoe ui", 22)

img_fundo = pygame.image.load("assets/images/fundodatela.jpeg").convert()
img_fundo = pygame.transform.scale(img_fundo, (LARGURA, ALTURA))

img_titulo = pygame.image.load("assets/images/titulo.1.png").convert_alpha()
largura_logo = 230
w, h = img_titulo.get_size()
altura_logo = int(largura_logo * h / w)
img_titulo = pygame.transform.smoothscale(img_titulo, (largura_logo, altura_logo))

sprites_robo = [
    pygame.image.load("assets/images/FRONT.1.PNG").convert_alpha(),
    pygame.image.load("assets/images/ESQUERDA.1.PNG").convert_alpha(),
    pygame.image.load("assets/images/ATRÁS.1.PNG").convert_alpha(),
    pygame.image.load("assets/images/DIREITA.1.PNG").convert_alpha()
]

for i in range(len(sprites_robo)):
    sprites_robo[i] = pygame.transform.scale(sprites_robo[i], (320, 320))

particulas = []
for i in range(120):
    particulas.append({
        "x": random.randint(0, LARGURA),
        "y": random.randint(0, ALTURA),
        "raio": random.randint(1, 3),
        "vel": random.uniform(0.2, 1.0)
    })

def desenhar_estrelas():
    for p in particulas:
        p["y"] -= p["vel"]
        if p["y"] < 0:
            p["y"] = ALTURA
            p["x"] = random.randint(0, LARGURA)
        pygame.draw.circle(tela, BRANCO, (int(p["x"]), int(p["y"])), p["raio"])

def desenhar_perfil(mouse):
    rect = pygame.Rect(1160, 22, 55, 55)
    hover = rect.collidepoint(mouse)
    fundo = pygame.Surface((55, 55), pygame.SRCALPHA)
    pygame.draw.rect(
        fundo,
        (255, 255, 255, 35) if hover else (255, 255, 255, 18),
        fundo.get_rect(),
        border_radius=20
    )
    tela.blit(fundo, (1160, 22))
    pygame.draw.rect(tela, AZUL_CLARO, rect, 2, border_radius=20)
    pygame.draw.circle(tela, BRANCO, (1187, 42), 8)
    pygame.draw.arc(tela, BRANCO, (1173, 47, 28, 22), 0, 3.14, 2)

def desenhar_botao(x, y, texto, mouse, superficie_destino=tela):
    rect = pygame.Rect(x, y, 120, 42)
    hover = rect.collidepoint(mouse)
    fundo = pygame.Surface((120, 42), pygame.SRCALPHA)
    pygame.draw.rect(
        fundo,
        (255, 255, 255, 45) if hover else (255, 255, 255, 20),
        fundo.get_rect(),
        border_radius=15
    )
    superficie_destino.blit(fundo, (x, y))
    pygame.draw.rect(superficie_destino, AZUL_CLARO, rect, 2, border_radius=15)
    txt = fonte_botao.render(texto, True, BRANCO)
    superficie_destino.blit(txt, txt.get_rect(center=rect.center))
    return rect

def desenhar_card(x, y, titulo, subtitulo, mouse):
    largura = 230
    altura = 300
    rect = pygame.Rect(x, y, largura, altura)
    hover = rect.collidepoint(mouse)
    brilho = pygame.Surface((250, 320), pygame.SRCALPHA)
    pygame.draw.rect(
        brilho,
        (80, 120, 255, 70) if hover else (80, 120, 255, 35),
        brilho.get_rect(),
        border_radius=30
    )
    tela.blit(brilho, (x - 10, y - 10))
    fundo = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(fundo, (8, 18, 55, 215), fundo.get_rect(), border_radius=28)
    tela.blit(fundo, (x, y))
    pygame.draw.rect(tela, AZUL_CLARO, rect, 3, border_radius=28)
    topo = pygame.Surface((largura, 58), pygame.SRCALPHA)
    pygame.draw.rect(topo, (45, 70, 180, 180), topo.get_rect(), border_radius=28)
    tela.blit(topo, (x, y))
    tamanho = 22
    if len(titulo) > 14: tamanho = 18
    if len(titulo) > 18: tamanho = 16
    fonte = pygame.font.SysFont("bahnschrift", tamanho, bold=True)
    txt = fonte.render(titulo, True, BRANCO)
    tela.blit(txt, txt.get_rect(center=(x + 115, y + 30)))
    pygame.draw.rect(tela, AZUL_CLARO, (x + 92, y + 110, 46, 62), 2)
    sub = fonte_sub.render(subtitulo, True, (190, 200, 255))
    tela.blit(sub, sub.get_rect(center=(x + 115, y + 205)))
    botao = desenhar_botao(x + 55, y + 240, "INICIAR", mouse)
    return botao

def desenhar_robo(tempo):
    frame = int(tempo * 0.5) % len(sprites_robo)
    robo = sprites_robo[frame]
    offset_y = math.sin(tempo * 2) * 10
    offset_x = math.sin(tempo) * 5
    x = 70 + offset_x
    y = 190 + offset_y
    luz = pygame.Surface((260, 80), pygame.SRCALPHA)
    pygame.draw.ellipse(luz, (90, 140, 255, 90), (0, 0, 260, 80))
    tela.blit(luz, (x + 40, y + 250))
    luz2 = pygame.Surface((180, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(luz2, (180, 220, 255, 70), (0, 0, 180, 40))
    tela.blit(luz2, (x + 80, y + 270))
    rect = robo.get_rect(center=(x + 160, y + 170))
    tela.blit(robo, rect)

def desenhar_nivel(x, y, numero, mouse):
    rect = pygame.Rect(x, y, 100, 100)
    hover = rect.collidepoint(mouse)
    fundo = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.rect(
        fundo,
        (255, 255, 255, 40) if hover else (8, 18, 55, 215),
        fundo.get_rect(),
        border_radius=22
    )
    tela.blit(fundo, (x, y))
    pygame.draw.rect(tela, AZUL_CLARO, rect, 3, border_radius=22)
    txt = fonte_card.render(f"1-{numero}", True, BRANCO)
    tela.blit(txt, txt.get_rect(center=rect.center))
    return rect

def tela_menu(mouse, tempo):
    tela.blit(img_fundo, (0, 0))
    desenhar_estrelas()
    tela.blit(img_titulo, (30, 18))
    desenhar_perfil(mouse)
    titulo = fonte_titulo.render("Pense, treine e PERSISTA!", True, BRANCO)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 112)))
    pygame.draw.line(tela, AZUL_CLARO, (300, 174), (980, 174), 3)
    desenhar_robo(tempo)
    btn_port = desenhar_card(390, 260, "CÓDICES LETRAIS", "Leitura e interpretação", mouse)
    btn_mat = desenhar_card(660, 260, "SUSSURROS NUMÉRICOS", "Desafios e lógica", mouse)
    btn_aux = desenhar_card(930, 260, "AUXILIADOR", "Peça ajuda", mouse)
    return btn_port, btn_mat, btn_aux

def tela_estagios(mouse, titulo_texto):
    tela.blit(img_fundo, (0, 0))
    desenhar_estrelas()
    tela.blit(img_titulo, (30, 18))
    titulo = fonte_titulo.render(titulo_texto, True, BRANCO)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 95)))
    inicio_x = 390
    inicio_y = 230
    numero = 1
    nivel_rects = []
    for linha in range(3):
        for coluna in range(4):
            x = inicio_x + coluna * 130
            y = inicio_y + linha * 130
            rect = desenhar_nivel(x, y, numero, mouse)
            nivel_rects.append((numero, rect))
            numero += 1
    voltar = desenhar_botao(40, 640, "VOLTAR", mouse)
    return voltar, nivel_rects

def tela_auxiliador(mouse, serie_escolhida):
    global scroll_y
    tela.blit(img_fundo, (0, 0))
    desenhar_estrelas()
    tela.blit(img_titulo, (30, 18))
    titulo = fonte_titulo.render("AUXILIADOR", True, BRANCO)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 90)))
    pygame.draw.line(tela, AZUL_CLARO, (300, 175), (980, 175), 3)
    voltar = desenhar_botao(40, 640, "VOLTAR", mouse)
    if serie_escolhida is None:
        subtitulo = fonte_sub.render("Escolha sua série", True, (190, 200, 255))
        tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 145)))
        serie1 = desenhar_botao(360, 230, "1º ANO", mouse)
        serie2 = desenhar_botao(560, 230, "2º ANO", mouse)
        serie3 = desenhar_botao(760, 230, "3º ANO", mouse)
        return voltar, serie1, serie2, serie3, []
    serie1 = serie2 = serie3 = None
    subtitulo = fonte_sub.render(f"Série selecionada: {serie_escolhida}", True, (190, 200, 255))
    tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 145)))
    caixa = pygame.Surface((900, 470), pygame.SRCALPHA)
    pygame.draw.rect(caixa, (8, 18, 55, 215), caixa.get_rect(), border_radius=28)
    tela.blit(caixa, (190, 210))
    pygame.draw.rect(tela, AZUL_CLARO, (190, 210, 900, 470), 3, border_radius=28)
    titulo_lista = fonte_card.render("MONITORES DISPONÍVEIS", True, BRANCO)
    tela.blit(titulo_lista, titulo_lista.get_rect(center=(640, 245)))
    if serie_escolhida == "1º ANO" or serie_escolhida == "3º ANO":
        aviso = fonte_card.render("INDISPONÍVEL NO MOMENTO", True, (190, 200, 255))
        tela.blit(aviso, aviso.get_rect(center=(640, 430)))
        return voltar, serie1, serie2, serie3, []
    scroll_largura = 860
    scroll_altura = 380
    scroll_x_pos = 210
    scroll_y_pos = 280
    superficie_lista = pygame.Surface((scroll_largura, scroll_altura), pygame.SRCALPHA)
    superficie_lista.set_clip(pygame.Rect(0, 0, scroll_largura, scroll_altura))
    mouse_relativo = (mouse[0] - scroll_x_pos, mouse[1] - scroll_y_pos)
    linhas_matematica = [("Mallu", "MAT"), ("Luana", "MAT"), ("João", "MAT")]
    linhas_portugues = [("Everton", "PORT"), ("Maryna", "PORT"), ("Eloisa", "PORT"), ("Fernanda", "PORT")]
    colunas = ["MONITOR", "ÁREA", "STATUS"]
    posicoes = [110, 490, 640]
    botoes_chat = []
    y = 20 + scroll_y
    titulo_mat = fonte_card.render("MATEMÁTICA", True, BRANCO)
    superficie_lista.blit(titulo_mat, (90, y))
    y += 45
    for i, col in enumerate(colunas):
        txt = fonte_botao.render(col, True, BRANCO)
        superficie_lista.blit(txt, (posicoes[i], y))
    y += 48
    for monitor, area in linhas_matematica:
        monitor_txt = fonte_sub.render(monitor, True, (220, 225, 255))
        area_txt = fonte_sub.render(area, True, (220, 225, 255))
        superficie_lista.blit(monitor_txt, (posicoes[0], y))
        superficie_lista.blit(area_txt, (posicoes[1], y))
        chat = desenhar_botao(610, y - 8, "CHAT", mouse_relativo, superficie_lista)
        chat_global = chat.move(scroll_x_pos, scroll_y_pos)
        botoes_chat.append((chat_global, monitor))
        y += 52
    titulo_port = fonte_card.render("PORTUGUÊS", True, BRANCO)
    superficie_lista.blit(titulo_port, (90, y + 10))
    y += 55
    for i, col in enumerate(colunas):
        txt = fonte_botao.render(col, True, BRANCO)
        superficie_lista.blit(txt, (posicoes[i], y))
    y += 48
    for monitor, area in linhas_portugues:
        monitor_txt = fonte_sub.render(monitor, True, (220, 225, 255))
        area_txt = fonte_sub.render(area, True, (220, 225, 255))
        indisp = fonte_sub.render("INDISP.", True, (180, 190, 220))
        superficie_lista.blit(monitor_txt, (posicoes[0], y))
        superficie_lista.blit(area_txt, (posicoes[1], y))
        superficie_lista.blit(indisp, (posicoes[2], y))
        y += 52
    altura_total_conteudo = y - scroll_y
    max_scroll = min(0, scroll_altura - altura_total_conteudo - 40)
    if scroll_y < max_scroll: scroll_y = max_scroll
    if scroll_y > 0: scroll_y = 0
    tela.blit(superficie_lista, (scroll_x_pos, scroll_y_pos))
    return voltar, serie1, serie2, serie3, botoes_chat

def tela_chat(mouse, monitor_atual, mensagens_chat, texto_digitado):
    tela.blit(img_fundo, (0, 0))
    desenhar_estrelas()
    tela.blit(img_titulo, (30, 18))
    titulo = fonte_titulo.render(f"CHAT COM {monitor_atual.upper()}", True, BRANCO)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 90)))
    caixa = pygame.Surface((820, 430), pygame.SRCALPHA)
    pygame.draw.rect(caixa, (8, 18, 55, 220), caixa.get_rect(), border_radius=28)
    tela.blit(caixa, (230, 160))
    pygame.draw.rect(tela, AZUL_CLARO, (230, 160, 820, 430), 3, border_radius=28)
    y = 190
    for autor, msg in mensagens_chat[-8:]:
        if autor == "aluno":
            texto = fonte_sub.render("Você: " + msg, True, (220, 225, 255))
            tela.blit(texto, (520, y))
        elif autor == "monitor":
            texto = fonte_sub.render(monitor_atual + ": " + msg, True, (180, 220, 255))
            tela.blit(texto, (270, y))
        else:
            texto = fonte_sub.render(msg, True, (180, 190, 220))
            tela.blit(texto, (270, y))
        y += 45
    pygame.draw.rect(tela, (8, 18, 55), (250, 610, 720, 50), border_radius=18)
    pygame.draw.rect(tela, AZUL_CLARO, (250, 610, 720, 50), 2, border_radius=18)
    texto = fonte_sub.render(texto_digitado, True, BRANCO)
    tela.blit(texto, (270, 623))
    enviar = desenhar_botao(990, 615, "ENVIAR", mouse)
    voltar = desenhar_botao(40, 640, "VOLTAR", mouse)
    return voltar, enviar

tempo = 0
while True:
    tempo += 0.05
    mouse = pygame.mouse.get_pos()
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if estado == AUXILIADOR and serie_escolhida == "2º ANO":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if pygame.Rect(190, 280, 900, 380).collidepoint(mouse):
                    arrastando = True
                    mouse_y_anterior = mouse[1]
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                arrastando = False
            elif evento.type == pygame.MOUSEMOTION and arrastando:
                variacao_y = mouse[1] - mouse_y_anterior
                scroll_y += variacao_y
                mouse_y_anterior = mouse[1]
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 4: scroll_y += 25
                elif evento.button == 5: scroll_y -= 25

    if estado == MENU:
        btn_port, btn_mat, btn_aux = tela_menu(mouse, tempo)
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if btn_port.collidepoint(mouse): estado = PORTUGUES
                elif btn_mat.collidepoint(mouse): estado = MATEMATICA
                elif btn_aux.collidepoint(mouse):
                    estado = AUXILIADOR
                    serie_escolhida = None
                    scroll_y = 0

    elif estado == PORTUGUES:
        voltar, niveis = tela_estagios(mouse, "CÓDICES LETRAIS")
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if voltar.collidepoint(mouse): estado = MENU
                for numero, rect in niveis:
                    if rect.collidepoint(mouse):
                        if numero == 1: subprocess.run(["python", "games/robo_detector.py"])

    elif estado == MATEMATICA:
        voltar, niveis = tela_estagios(mouse, "SUSSURROS NUMÉRICOS")
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if voltar.collidepoint(mouse): estado = MENU
                for numero, rect in niveis:
                    if rect.collidepoint(mouse):
                        if numero == 1: subprocess.run(["python", "games/matematica.py"])
                        else: print(f"Fase {numero} ainda não criada.")

    elif estado == AUXILIADOR:
        voltar, serie1, serie2, serie3, botoes_chat = tela_auxiliador(mouse, serie_escolhida)
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if voltar.collidepoint(mouse): estado = MENU
                if serie1 and serie1.collidepoint(mouse): serie_escolhida = "1º ANO"
                elif serie2 and serie2.collidepoint(mouse):
                    serie_escolhida = "2º ANO"
                    scroll_y = 0
                elif serie3 and serie3.collidepoint(mouse): serie_escolhida = "3º ANO"
                for botao, monitor in botoes_chat:
                    if botao.collidepoint(mouse):
                        estado = CHAT
                        monitor_atual = monitor
                        mensagens_chat = [("sistema", f"Chat iniciado com {monitor_atual}. Digite sua dúvida.")]
                        texto_digitado = ""
                        tempo_resposta = None

    elif estado == CHAT:
        voltar, enviar = tela_chat(mouse, monitor_atual, mensagens_chat, texto_digitado)
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if voltar.collidepoint(mouse): estado = AUXILIADOR
                elif enviar.collidepoint(mouse):
                    if texto_digitado.strip() != "":
                        mensagens_chat.append(("aluno", texto_digitado.strip()))
                        mensagens_chat.append(("sistema", "Mensagem enviada. Aguardando resposta..."))
                        texto_digitado = ""
                        tempo_resposta = pygame.time.get_ticks()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE: texto_digitado = texto_digitado[:-1]
                elif evento.key == pygame.K_RETURN:
                    if texto_digitado.strip() != "":
                        mensagens_chat.append(("aluno", texto_digitado.strip()))
                        mensagens_chat.append(("sistema", "Mensagem enviada. Aguardando resposta..."))
                        texto_digitado = ""
                        tempo_resposta = pygame.time.get_ticks()
                else: texto_digitado += evento.unicode
        if tempo_resposta is not None:
            if pygame.time.get_ticks() - tempo_resposta > 2500:
                mensagens_chat.append(("monitor", "Recebi sua dúvida! Já vou te ajudar."))
                tempo_resposta = None

    pygame.display.update()
    relogio.tick(60)