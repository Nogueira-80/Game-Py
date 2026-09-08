import pygame
import os
import random

# =========================================================
# INICIALIZAÇÃO
# =========================================================

pygame.init()

TELA_LARGURA = 500
TELA_ALTURA = 800

# =========================================================
# IMAGENS
# =========================================================

IMAGEM_CANO = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'pipe.png'))
)

IMAGEM_CHAO = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'base.png'))
)

IMAGEM_BACKGROUND = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'bg.png'))
)

IMAGENS_PASSARO = [
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('imgs', 'bird1.png'))
    ),
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('imgs', 'bird2.png'))
    ),
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('imgs', 'bird3.png'))
    )
]

# =========================================================
# FONTE
# =========================================================

FONTE_PONTOS = pygame.font.SysFont('arial', 40)
FONTE_GAME_OVER = pygame.font.SysFont('arial', 50)
FONTE_REINICIAR = pygame.font.SysFont('arial', 25)


# =========================================================
# CLASSE DO PASSARINHO
# =========================================================

class Passaro:

    IMGS = IMAGENS_PASSARO

    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.angulo = 0

        # Velocidade vertical
        self.velocidade = 0

        # Controle da animação
        self.contagem_imagem = 0

        self.imagem = self.IMGS[0]

    # -----------------------------------------------------
    # PULO
    # -----------------------------------------------------

    def pular(self):

        # Velocidade negativa = subir
        self.velocidade = -10

    # -----------------------------------------------------
    # MOVIMENTO
    # -----------------------------------------------------

    def mover(self):

        # Gravidade
        self.velocidade += 0.5

        # Movimenta o pássaro
        self.y += self.velocidade

        # Se estiver subindo
        if self.velocidade < 0:

            self.angulo = 25

        # Se estiver caindo
        else:

            self.angulo -= 5

            if self.angulo < -90:
                self.angulo = -90

    # -----------------------------------------------------
    # DESENHAR PASSARINHO
    # -----------------------------------------------------

    def desenhar(self, tela):

        # Controle da animação das asas
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:

            self.imagem = self.IMGS[0]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:

            self.imagem = self.IMGS[1]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:

            self.imagem = self.IMGS[2]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:

            self.imagem = self.IMGS[1]

        else:

            self.imagem = self.IMGS[0]

            self.contagem_imagem = 0

        # Quando estiver caindo muito,
        # mantém uma imagem específica
        if self.angulo <= -80:

            self.imagem = self.IMGS[1]

        # Rotaciona a imagem
        imagem_rotacionada = pygame.transform.rotate(
            self.imagem,
            self.angulo
        )

        # Descobre o centro da imagem original
        pos_centro_imagem = self.imagem.get_rect(
            topleft=(self.x, self.y)
        ).center

        # Cria o retângulo da imagem rotacionada
        retangulo = imagem_rotacionada.get_rect(
            center=pos_centro_imagem
        )

        # Desenha na tela
        tela.blit(
            imagem_rotacionada,
            retangulo.topleft
        )

    # -----------------------------------------------------
    # MÁSCARA DE COLISÃO
    # -----------------------------------------------------

    def get_mask(self):

        return pygame.mask.from_surface(self.imagem)


# =========================================================
# CLASSE DOS CANOS
# =========================================================

class Cano:

    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):

        self.x = x

        self.altura = 0

        self.pos_topo = 0
        self.pos_base = 0

        self.CANO_TOPO = pygame.transform.flip(
            IMAGEM_CANO,
            False,
            True
        )

        self.CANO_BASE = IMAGEM_CANO

        self.passou = False

        self.definir_altura()

    # -----------------------------------------------------
    # DEFINIR ALTURA DOS CANOS
    # -----------------------------------------------------

    def definir_altura(self):

        self.altura = random.randrange(50, 450)

        self.pos_topo = (
            self.altura -
            self.CANO_TOPO.get_height()
        )

        self.pos_base = (
            self.altura +
            self.DISTANCIA
        )

    # -----------------------------------------------------
    # MOVIMENTAR CANO
    # -----------------------------------------------------

    def mover(self):

        self.x -= self.VELOCIDADE

    # -----------------------------------------------------
    # DESENHAR CANOS
    # -----------------------------------------------------

    def desenhar(self, tela):

        tela.blit(
            self.CANO_TOPO,
            (self.x, self.pos_topo)
        )

        tela.blit(
            self.CANO_BASE,
            (self.x, self.pos_base)
        )

    # -----------------------------------------------------
    # VERIFICAR COLISÃO
    # -----------------------------------------------------

    def colidir(self, passaro):

        passaro_mask = passaro.get_mask()

        topo_mask = pygame.mask.from_surface(
            self.CANO_TOPO
        )

        base_mask = pygame.mask.from_surface(
            self.CANO_BASE
        )

        distancia_topo = (
            self.x - passaro.x,
            self.pos_topo - round(passaro.y)
        )

        distancia_base = (
            self.x - passaro.x,
            self.pos_base - round(passaro.y)
        )

        topo_ponto = passaro_mask.overlap(
            topo_mask,
            distancia_topo
        )

        base_ponto = passaro_mask.overlap(
            base_mask,
            distancia_base
        )

        if topo_ponto or base_ponto:

            return True

        return False


# =========================================================
# CLASSE DO CHÃO
# =========================================================

class Chao:

    VELOCIDADE = 5

    LARGURA = IMAGEM_CHAO.get_width()

    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):

        self.y = y

        self.x1 = 0

        self.x2 = self.LARGURA

    # -----------------------------------------------------
    # MOVIMENTAR CHÃO
    # -----------------------------------------------------

    def mover(self):

        self.x1 -= self.VELOCIDADE

        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:

            self.x1 = self.x2 + self.LARGURA

        if self.x2 + self.LARGURA < 0:

            self.x2 = self.x1 + self.LARGURA

    # -----------------------------------------------------
    # DESENHAR CHÃO
    # -----------------------------------------------------

    def desenhar(self, tela):

        tela.blit(
            self.IMAGEM,
            (self.x1, self.y)
        )

        tela.blit(
            self.IMAGEM,
            (self.x2, self.y)
        )


# =========================================================
# DESENHAR TELA
# =========================================================

def desenhar_tela(
    tela,
    passaros,
    canos,
    chao,
    pontos
):

    # Fundo
    tela.blit(
        IMAGEM_BACKGROUND,
        (0, 0)
    )

    # Canos
    for cano in canos:

        cano.desenhar(tela)

    # Passarinho
    for passaro in passaros:

        passaro.desenhar(tela)

    # Pontuação
    texto = FONTE_PONTOS.render(
        f"Pontuação: {pontos}",
        True,
        (255, 255, 255)
    )

    tela.blit(
        texto,
        (
            TELA_LARGURA -
            texto.get_width() -
            10,
            10
        )
    )

    # Chão
    chao.desenhar(tela)

    # Atualiza tela
    pygame.display.update()


# =========================================================
# TELA GAME OVER
# =========================================================

def tela_game_over(
    tela,
    pontos
):

    tela.fill((0, 0, 0))

    texto_game_over = FONTE_GAME_OVER.render(
        "GAME OVER",
        True,
        (255, 255, 255)
    )

    texto_pontos = FONTE_PONTOS.render(
        f"Pontuação: {pontos}",
        True,
        (255, 255, 255)
    )

    texto_reiniciar = FONTE_REINICIAR.render(
        "Pressione R para jogar novamente",
        True,
        (255, 255, 255)
    )

    tela.blit(
        texto_game_over,
        (
            TELA_LARGURA // 2 -
            texto_game_over.get_width() // 2,
            250
        )
    )

    tela.blit(
        texto_pontos,
        (
            TELA_LARGURA // 2 -
            texto_pontos.get_width() // 2,
            330
        )
    )

    tela.blit(
        texto_reiniciar,
        (
            TELA_LARGURA // 2 -
            texto_reiniciar.get_width() // 2,
            400
        )
    )

    pygame.display.update()


# =========================================================
# JOGO
# =========================================================

def jogar():

    # -----------------------------------------------------
    # OBJETOS
    # -----------------------------------------------------

    passaros = [
        Passaro(230, 350)
    ]

    chao = Chao(730)

    canos = [
        Cano(700)
    ]

    # -----------------------------------------------------
    # TELA
    # -----------------------------------------------------

    tela = pygame.display.set_mode(
        (
            TELA_LARGURA,
            TELA_ALTURA
        )
    )

    pygame.display.set_caption(
        "Flappy Bird - Python"
    )

    # -----------------------------------------------------
    # CONTROLE
    # -----------------------------------------------------

    pontos = 0

    relogio = pygame.time.Clock()

    rodando = True

    game_over = False

    # =====================================================
    # LOOP PRINCIPAL
    # =====================================================

    while rodando:

        relogio.tick(30)

        # =================================================
        # EVENTOS
        # =================================================

        for evento in pygame.event.get():

            # Fechar janela
            if evento.type == pygame.QUIT:

                rodando = False

            # Teclado
            if evento.type == pygame.KEYDOWN:

                # ESPAÇO = PULAR
                if evento.key == pygame.K_SPACE:

                    if not game_over:

                        passaros[0].pular()

                # R = REINICIAR
                if evento.key == pygame.K_r:

                    if game_over:

                        return True

        # =================================================
        # SE O JOGO ESTIVER RODANDO
        # =================================================

        if not game_over:

            passaro = passaros[0]

            # ---------------------------------------------
            # MOVIMENTAR PASSARINHO
            # ---------------------------------------------

            passaro.mover()

            # ---------------------------------------------
            # MOVIMENTAR CHÃO
            # ---------------------------------------------

            chao.mover()

            # ---------------------------------------------
            # CANOS
            # ---------------------------------------------

            adicionar_cano = False

            remover_canos = []

            for cano in canos:

                # Verificar colisão
                if cano.colidir(passaro):

                    game_over = True

                # Verificar se passou pelo cano
                if (
                    not cano.passou
                    and passaro.x > cano.x
                ):

                    cano.passou = True

                    adicionar_cano = True

                # Mover cano
                cano.mover()

                # Verificar se saiu da tela
                if (
                    cano.x +
                    cano.CANO_TOPO.get_width()
                    < 0
                ):

                    remover_canos.append(cano)

            # ---------------------------------------------
            # ADICIONAR NOVO CANO
            # ---------------------------------------------

            if adicionar_cano:

                pontos += 1

                canos.append(
                    Cano(600)
                )

            # ---------------------------------------------
            # REMOVER CANOS
            # ---------------------------------------------

            for cano in remover_canos:

                canos.remove(cano)

            # ---------------------------------------------
            # COLISÃO COM O CHÃO
            # ---------------------------------------------

            if (
                passaro.y +
                passaro.imagem.get_height()
                >= chao.y
            ):

                game_over = True

            # ---------------------------------------------
            # COLISÃO COM O TOPO
            # ---------------------------------------------

            if passaro.y < 0:

                game_over = True

        # =================================================
        # DESENHAR
        # =================================================

        if not game_over:

            desenhar_tela(
                tela,
                passaros,
                canos,
                chao,
                pontos
            )

        else:

            tela_game_over(
                tela,
                pontos
            )

    # =====================================================
    # FINALIZAR
    # =====================================================

    pygame.quit()

    return False


# =========================================================
# INICIAR JOGO
# =========================================================

while True:

    reiniciar = jogar()

    if not reiniciar:

        break