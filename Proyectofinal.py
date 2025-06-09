import pygame
import random
import time
import sys

pygame.init()

ancho, alto = 800, 700
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Menú")

titulo = pygame.font.SysFont("Arial", 32)
texto = pygame.font.SysFont("Arial", 28)
font_x = pygame.font.SysFont("Arial", 40, bold=True)

blanco = (255, 255, 255)
negro = (0, 0, 0)
gris = (200, 200, 200) 
azul = (50, 150, 255)
rojo = (255, 0, 0)
verde = (0, 200, 0)

reloj = pygame.time.Clock()

class CajaTexto:
    def __init__(self, x, y, ancho, alto, etiqueta):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = gris
        self.texto = ''
        self.etiqueta = etiqueta
        self.activa = False

    def manejarevento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.activa = self.rect.collidepoint(evento.pos)
            self.color = azul if self.activa else gris
        if evento.type == pygame.KEYDOWN and self.activa:
            if evento.key == pygame.K_RETURN:
                return self.texto
            elif evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                if len(self.texto) < 20:
                    self.texto += evento.unicode
        return None

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
        textorenderizado = texto.render(self.texto, True, negro)
        superficie.blit(textorenderizado, (self.rect.x + 10, self.rect.y + 10))
        etiquetarenderizada = titulo.render(self.etiqueta, True, negro)
        superficie.blit(etiquetarenderizada, (self.rect.x, self.rect.y - 35))
        pygame.draw.rect(superficie, negro, self.rect, 2)

cajastexto = [
    CajaTexto(250, 60, 300, 40, "Nombre del Jugador 1:"),
    CajaTexto(250, 140, 300, 40, "Nombre del Jugador 2:"),
    CajaTexto(250, 220, 300, 40, "Rondas por jugador:"),
    CajaTexto(250, 300, 300, 40, "Tamaño de cuadros de juego:")
]

tamanoboton = pygame.Rect(300, 400, 200, 50)

ejecutando = True
datosdelmenu = ["", "", "", ""]

while ejecutando:
    pantalla.fill(blanco)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for i, caja in enumerate(cajastexto):
            resultado = caja.manejarevento(evento)
            if resultado is not None:
                datosdelmenu[i] = resultado
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if tamanoboton.collidepoint(evento.pos):
                if all(d.strip() for d in datosdelmenu):
                    try:
                        int(datosdelmenu[2])
                        int(datosdelmenu[3])
                        ejecutando = False
                    except ValueError:
                        pass

    for caja in cajastexto:
        caja.dibujar(pantalla)

    pygame.draw.rect(pantalla, azul, tamanoboton)
    texto_boton = titulo.render("Iniciar Juego", True, blanco)
    pantalla.blit(texto_boton, (tamanoboton.x + 30, tamanoboton.y + 10))

    pygame.display.flip()
    reloj.tick(30)

p1, p2, rondas, tamanotablero = datosdelmenu
rondas = int(rondas)
n = int(tamanotablero)

cuadros = 60
ancho = n * cuadros
alto = n * cuadros
altoextra = 300
pantallajuego = pygame.display.set_mode((ancho, alto + altoextra))
pygame.display.set_caption("Matriz Aritmética")

matriz = [[random.randint(0, 11) for _ in range(n)] for _ in range(n)]
usados = set()
revelado = [[False for _ in range(n)] for _ in range(n)]

def numerosquerodean(f, c):
    vecinos = []
    for i in range(f - 1, f + 2):
        for j in range(c - 1, c + 2):
            if 0 <= i < n and 0 <= j < n and not (i == f and j == c):
                vecinos.append((i, j))
    return vecinos

def dibujartablero():
    for i in range(n):
        for j in range(n):
            x, y = j * cuadros, i * cuadros
            rect = pygame.Rect(x, y, cuadros, cuadros)
            pygame.draw.rect(pantallajuego, blanco, rect)
            if (i, j) in usados:
                pygame.draw.rect(pantallajuego, gris, rect)
                texto_x = font_x.render("X", True, negro)
                pantallajuego.blit(texto_x, (x + cuadros // 3, y + cuadros // 5))
            elif revelado[i][j]:
                texto_celda = texto.render(str(matriz[i][j]), True, azul)
                pantallajuego.blit(texto_celda, (x + cuadros // 3, y + cuadros // 3))
            else:
                pygame.draw.rect(pantallajuego, blanco, rect)
            pygame.draw.rect(pantallajuego, negro, rect, 2)

def mostrarmensaje(mensajes, opciones=None):
    pantallajuego.fill(blanco)
    dibujartablero()
    y_offset = alto + 10
    for mensaje in mensajes:
        texto_mensaje = texto.render(mensaje, True, negro)
        pantallajuego.blit(texto_mensaje, (10, y_offset))
        y_offset += 35
    if opciones:
        y_offset += 10
        for idx, op in enumerate(opciones):
            texto_opcion = texto.render(f"{idx+1}. {op}", True, negro)
            pantallajuego.blit(texto_opcion, (40, y_offset))
            y_offset += 35
    pygame.display.flip()

def esperaropcion(opciones):
    inicio = time.time()
    seleccion = None
    while time.time() - inicio < 25:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_4:
                    seleccion = event.key - pygame.K_0
        if seleccion and 1 <= seleccion <= 4:
            return seleccion
    return None

def turno(fila, col, jugador):
    if (fila, col) in usados:
        return 0
    usados.add((fila, col))
    revelado[fila][col] = True
    vecinos = numerosquerodean(fila, col)
    for i, j in vecinos:
        revelado[i][j] = True

    valor = matriz[fila][col]
    suma = sum(matriz[i][j] for i, j in vecinos)
    resultado = valor * suma

    opciones = [resultado]
    while len(opciones) < 4:
        o = resultado + random.randint(-20, 20)
        if o >= 0 and o not in opciones:
            opciones.append(o)
    random.shuffle(opciones)

    mostrarmensaje([
        f"Turno de {jugador}",
        f"Seleccionaste: {valor}",
        "Selecciona la opción correcta:"], opciones)

    seleccion = esperaropcion(opciones)

    if seleccion is None:
        mostrarmensaje(["Tiempo agotado."])
        pygame.time.delay(1500)
        return 0
    elif opciones[seleccion - 1] == resultado:
        mostrarmensaje(["Correcto. +3 puntos."])
        pygame.time.delay(1500)
        return 3
    else:
        mostrarmensaje([f"Incorrecto. Era {resultado}."])
        pygame.time.delay(1500)
        return 0

def reiniciar_tablero():
    for i in range(n):
        for j in range(n):
            if (i, j) not in usados:
                revelado[i][j] = False

jugadores = p1, p2
puntos = [0, 0]
turnoactual = 0
jugada = 0

while jugada < rondas * 2:
    pantallajuego.fill(blanco)
    dibujartablero()
    mostrarmensaje([f"Esperando clic de {jugadores[turnoactual]}..."])

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                fila, col = y // cuadros, x // cuadros
                if fila < n and col < n and (fila, col) not in usados:
                    puntos[turnoactual] += turno(fila, col, jugadores[turnoactual])
                    reiniciar_tablero()
                    turnoactual = 1 - turnoactual
                    jugada += 1
                    esperando = False

punteos = [f"{jugadores[0]}: {puntos[0]} puntos", f"{jugadores[1]}: {puntos[1]} puntos"]
if puntos[0] > puntos[1]:
    punteos.append(f"Ganador: {jugadores[0]}")
elif puntos[1] > puntos[0]:
    punteos.append(f"Ganador: {jugadores[1]}")
else:
    punteos.append("Empate")

mostrarmensaje(["Juego terminado"] + punteos)
pygame.time.delay(8000)
pygame.quit()
