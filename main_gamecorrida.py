import pygame
import sys
import math


pygame.init()

# ==============================
# CONFIGURAÇÕES DA TELA
# ==============================
largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("FORÇA HORIZONTAL")



# ================== CONFIGURAÇÃO DA PISTA ==================
inicio_pista = -2000
tamanho_segmento = 100
quantidade_segmentos = 120
largura_pista = 400
x_pista = 200


# ================== PISTA ==================
pista = []
y = -4000  # tento fazer a pista ter o maior percurso possivel


for i in range(50):  # quantidade de blocos (tamanho da pista)
    pista.append((200, y, 400, 100))
    y += 100


# ==============================
# CARREGAMENTO DE ASSETS (IMAGENS)
# ==============================
# Imagem do jogador
carro_img = pygame.image.load("assets/carro.png")
escala_carro = 0.1

# Imagem do inimigo
inimigo_img_original = pygame.image.load("assets/carro_inimigo.png")
escala_inimigo = 0.2


# ================== DIMENSÕES E ESCALA ==================
# Base para redimensionamento
largura_original = carro_img.get_width()
altura_original = carro_img.get_height()

# ESCALA: cálculo do tamanho atual
escala = 1.0
largura_carro = int(largura_original * escala)
altura_carro = int(altura_original * escala)


# ==============================
# CONFIGURAÇÃO DO JOGADOR (CARRO)
# ==============================
carro_x = largura //2
carro_y = pista[-1][1] + 50

# Controle de deslocamento do mapa (simula movimento)
mapa_x = 0
mapa_y = 0

velocidade_base = 8
velocidade = velocidade_base

# ROTAÇÃO
angulo = 0

# FLIP: (espelhamento)
flip_x = False
flip_y = False


# ==============================
# CONFIGURAÇÃO DO INIMIGO
# ==============================
# Posição inicial do inimigo
inimigo_x = largura // 2 + 50
inimigo_y = pista[-1][1] + 100

velocidade_inimigo = 7


# ==============================
# FUNÇÃO DE RESET DO JOGO
# ==============================
def resetar_jogo():
    global carro_x, carro_y, inimigo_x, inimigo_y, angulo, vencedor

    # Reinicia posição do jogador
    carro_x = largura // 2
    carro_y = pista[-1][1] + 50

    # Reinicia posição do inimigo
    inimigo_x = largura // 2 + 50
    inimigo_y = pista[-1][1] + 100

    # Reinicia estado das transformações
    angulo = 0

    # Reinicia estado do jogo
    vencedor = None


# Armazena quem venceu a corrida
vencedor = None  # Pode ser "player" ou "inimigo"


clock = pygame.time.Clock() #Controle de FPS


while True:

    # ================== EVENTOS ==================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and vencedor is not None:
                resetar_jogo()

            
            # TRANSFORMAÇÃO: FLIP (espelhamento da imagem)
            if event.key == pygame.K_f:
                flip_x = not flip_x


            if event.key == pygame.K_g:
                flip_y = not flip_y


    # ================== ENTRADA CONTÍNUA =================
    teclas = pygame.key.get_pressed()

    # ================== MOVIMENTO DO JOGADOR ==================
    if vencedor is None:


         # TRANSFORMAÇÃO: TRANSLAÇÃO (movimento baseado no ângulo)
        if teclas[pygame.K_w]:
            carro_x -= math.sin(math.radians(angulo)) * velocidade
            carro_y -= math.cos(math.radians(angulo)) * velocidade


        if teclas[pygame.K_s]:  
            carro_x += math.sin(math.radians(angulo)) * velocidade
            carro_y += math.cos(math.radians(angulo)) * velocidade


        # TRANSFORMAÇÃO: ROTAÇÃO (alteração do ângulo do objeto)
        if teclas[pygame.K_a]:
             angulo += 5


        if teclas[pygame.K_d]:
            angulo -= 5



    # ================== IA DO INIMIGO ==================
    if vencedor is None:
        


        # movimento automático (translação simples)
        inimigo_y -= velocidade_inimigo


        # centralização na pista
        centro_pista = 200 + 400 // 2

        if inimigo_x < centro_pista:
            inimigo_x += 2
        elif inimigo_x > centro_pista:
            inimigo_x -= 2


    # ================== CONTROLE DE ESCALA ==================
    # TRANSFORMAÇÃO: ESCALA (zoom do objeto)
    if teclas[pygame.K_z]:
        escala += 0.01

    if teclas[pygame.K_x]:
        escala -= 0.01


    #limitar zoom
    if escala < 0.8:
        escala = 0.8
   
    if escala > 1.5:
        escala = 1.5


    clock.tick(60) #limitador de fps

    # TRANSFORMAÇÃO: TRANSLAÇÃO (câmera acompanha o carro)
    camera_x = carro_x - (largura // 2) / escala
    camera_y = carro_y - (altura // 2) / escala


    #SISTEMA DA VELOCIDADE DIMINUIR FORA DA PISTA
    dentro_da_pista = False

    for segmento in pista:
        x, y, w, h = segmento
        if x < carro_x < x + w and y < carro_y < y + h:
            dentro_da_pista = True

    if not dentro_da_pista:
        velocidade = velocidade_base * 2  # reduz fora da pista
    else:
        velocidade = velocidade_base


    
    # TRANSFORMAÇÃO: FLIP (espelhamento da imagem)
    carro_flipado = pygame.transform.flip(carro_img, flip_x, flip_y)


    # fundo do mapa
    for i in range(-10000, 10000, 100):
            cor = (34, 139, 34) if (i // 100) % 2 == 0 else (0, 100, 0)


            pygame.draw.rect(
            tela,
            cor,
            (
                0,
                (i - camera_y) * escala,
                largura,
                100 * escala
            )
    )


    # ================== DESENHO DA PISTA ==================
    for segmento in pista:
        x, y, w, h = segmento


        # pista
        pygame.draw.rect(
        tela,
        (50, 50, 50),
        ((x - camera_x) * escala, (y - camera_y) * escala, w * escala, h * escala)
    )


    # borda esquerda
        pygame.draw.rect(
            tela,
            (255, 255, 0),
            ((x - camera_x) * escala, (y - camera_y) * escala, 5 * escala, h * escala)
    )


    # borda direita
        pygame.draw.rect(
            tela,
            (255, 255, 0),
            ((x + w - 5 - camera_x) * escala, (y - camera_y) * escala, 5 * escala, h * escala)
    )


    # linha central
        for i in range(y, y + h, 40):
            pygame.draw.rect(
                tela,
                (255, 255, 255),
                ((x + w//2 - 5 - camera_x) * escala, (i - camera_y) * escala, 10 * escala, 20 * escala)
        )


    # ================== LINHA DE CHEGADA ==================
    y_chegada = pista[0][1]  # topo da pista


    for i in range(x_pista, x_pista + largura_pista, 20):
        for j in range(y_chegada, y_chegada + 40, 20):
            if (i // 20 + j // 20) % 2 == 0:
                pygame.draw.rect(
                    tela,
                    (255, 255, 255),
                    ((i - camera_x) * escala, (j - camera_y) * escala, 20 * escala, 20 * escala)
                )
   


    # ================== PORTAL DE CHEGADA ==================
    pygame.draw.rect(
        tela,
        (255, 255, 255),
    (
        (x_pista - camera_x) * escala,
        (y_chegada - 80 - camera_y) * escala,
        largura_pista * escala,
        10 * escala
    )
)


    # ================== TEXTO "FINISH" ==================
    fonte_finish = pygame.font.SysFont(None, 50)


    texto_finish = fonte_finish.render("FINISH", True, (255, 255, 255))


    # posição central do portal
    texto_x = x_pista + largura_pista // 2
    texto_y = y_chegada - 60


    # aplicar câmera
    tela.blit(
        texto_finish,
    (
            (texto_x - texto_finish.get_width() // 2 - camera_x) * escala,
            (texto_y - camera_y) * escala
    )
)


    # colunas laterais
    pygame.draw.rect(
        tela,
        (255, 255, 255),
        (
            (x_pista - camera_x) * escala,
            (y_chegada - 80 - camera_y) * escala,
            10 * escala,
            80 * escala
    )
)


    pygame.draw.rect(
        tela,
        (255, 255, 255),
        (
            (x_pista + largura_pista - 10 - camera_x) * escala,
            (y_chegada - 80 - camera_y) * escala,
            10 * escala,
            80 * escala
        )
)


    # ===== SISTEMA DE VITÓRIA =====
    if vencedor is None:


    # inimigo chegou primeiro → você perdeu
        if inimigo_y <= y_chegada:
            vencedor = "inimigo"


    # só verifica player se ninguém venceu ainda
        elif carro_y <= y_chegada:
            vencedor = "player"
   

    # TRANSFORMAÇÃO: ROTAÇÃO (gira a imagem do carro)
    carro_rotacionado = pygame.transform.rotate(carro_flipado, angulo)

    # TRANSFORMAÇÃO: ESCALA (redimensiona a imagem do carro)
    carro_zoom = pygame.transform.scale(
        carro_rotacionado,
    (
        int(carro_rotacionado.get_width() * escala * escala_carro),
        int(carro_rotacionado.get_height() * escala * escala_carro)
    )
)



    # desenhar carro player
    rect = carro_zoom.get_rect(center=(largura//2, altura//2))
    tela.blit(carro_zoom, rect)


    # ===== DESENHAR INIMIGO =====

    # TRANSFORMAÇÃO: ROTAÇÃO (inimigo)
    inimigo_rotacionado = pygame.transform.rotate(inimigo_img_original, 0)

    # TRANSFORMAÇÃO: ESCALA (inimigo)
    inimigo_zoom = pygame.transform.scale(
        inimigo_rotacionado,
    (
        int(inimigo_rotacionado.get_width() * escala * escala_inimigo),
        int(inimigo_rotacionado.get_height() * escala * escala_inimigo)
    )
)

    # posição na tela (considerando câmera)
    tela_x = (inimigo_x - camera_x) * escala
    tela_y = (inimigo_y - camera_y) * escala


    rect_inimigo = inimigo_zoom.get_rect(center=(tela_x, tela_y))
    tela.blit(inimigo_zoom, rect_inimigo)



    # ===== TELA DE VITÓRIA =====
    if vencedor is not None:
        fonte = pygame.font.SysFont(None, 60)
        fonte_menor = pygame.font.SysFont(None, 30)


        if vencedor == "player":
            texto = fonte.render("VOCE VENCEU!", True, (255, 255, 255))
        else:
            texto = fonte.render("VOCE PERDEU!", True, (255, 0, 0))


        texto_reiniciar = fonte_menor.render("Pressione R para reiniciar", True, (200, 200, 200))


        rect_texto = texto.get_rect(center=(largura//2, altura//2))
        rect_reiniciar = texto_reiniciar.get_rect(center=(largura//2, altura//2 + 60))


        # fundo escuro
        overlay = pygame.Surface((largura, altura))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))


        tela.blit(texto, rect_texto)
        tela.blit(texto_reiniciar, rect_reiniciar)


    pygame.display.update()