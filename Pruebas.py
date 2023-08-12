import pygame
import random
import sys

pygame.init()

ancho = 800
alto = 600

info_pantalla = pygame.display.Info()
ancho = info_pantalla.current_w
alto = info_pantalla.current_h

color_fondo = (0, 0, 0)

ventana = pygame.display.set_mode((ancho, alto), pygame.FULLSCREEN)
pygame.display.set_caption("Aventura de Cubos")

imagen_icono = pygame.image.load(r"Texturas/alienfachero.png")
pygame.display.set_icon(imagen_icono)

tamano_cubo = 100
x_cubo = ancho // 2 - tamano_cubo // 2
y_cubo = alto - tamano_cubo
velocidad_cubo = 1

tamano_bloque = 150
x_bloque = random.randint(0, ancho - tamano_bloque)
y_bloque = random.randint(0, alto - tamano_bloque)
velocidad_bloque = 0.7

fuente = pygame.font.Font(None, 36)
contador = 0
inicio_tiempo = pygame.time.get_ticks()

ultimo_tiempo_contador = pygame.time.get_ticks()
ultimo_tiempo_bloque = pygame.time.get_ticks()
intervalo_aumento_velocidad_bloque = 60000
intervalo_bloque_adicional = 30000

direccion_bloque = random.choice(["arriba", "abajo", "izquierda", "derecha"])
intervalo_cambio_direccion_bloque = random.randint(1500, 2000)
ultimo_tiempo_cambio_direccion = pygame.time.get_ticks()

bloques_adicionales = []

textura_cubo_rojo = pygame.image.load(r"Texturas/alienfachero.png").convert_alpha()
textura_cubo_rojo = pygame.transform.scale(textura_cubo_rojo, (tamano_cubo, tamano_cubo))

textura_bloque = pygame.image.load(r"Texturas/piedra con graficasos.png").convert_alpha()
textura_bloque = pygame.transform.scale(textura_bloque, (tamano_bloque, tamano_bloque))

musica = pygame.mixer.Sound(r"Audios/Musicaparacubocubico.mp3")
musica.play(-1)

def reiniciar_juego():
    global x_cubo, y_cubo, contador, ultimo_tiempo_contador, ultimo_tiempo_bloque, ultimo_tiempo_cambio_direccion
    x_cubo = ancho // 2 - tamano_cubo // 2
    y_cubo = alto - tamano_cubo
    contador = 0
    ultimo_tiempo_contador = pygame.time.get_ticks()
    ultimo_tiempo_bloque = pygame.time.get_ticks()
    ultimo_tiempo_cambio_direccion = pygame.time.get_ticks()
    bloques_adicionales.clear()

def bucle_juego():
    global x_cubo, y_cubo, velocidad_cubo, x_bloque, y_bloque, velocidad_bloque, direccion_bloque, ultimo_tiempo_bloque, bloques_adicionales, ultimo_tiempo_contador, intervalo_aumento_velocidad_bloque, inicio_tiempo, contador, ultimo_tiempo_cambio_direccion,intervalo_cambio_direccion_bloque

    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_w] and y_cubo > 0:
            y_cubo -= velocidad_cubo
        if teclas[pygame.K_s] and y_cubo < alto - tamano_cubo:
            y_cubo += velocidad_cubo
        if teclas[pygame.K_a] and x_cubo > 0:
            x_cubo -= velocidad_cubo
        if teclas[pygame.K_d] and x_cubo < ancho - tamano_cubo:
            x_cubo += velocidad_cubo

        tiempo_actual_contador = pygame.time.get_ticks()
        if tiempo_actual_contador - ultimo_tiempo_contador >= 1000:
            contador += 1
            ultimo_tiempo_contador = tiempo_actual_contador

        tiempo_actual_bloque = pygame.time.get_ticks()
        if tiempo_actual_bloque - ultimo_tiempo_bloque >= intervalo_aumento_velocidad_bloque:
            velocidad_bloque += 0.1
            ultimo_tiempo_bloque = tiempo_actual_bloque

        if tiempo_actual_bloque - ultimo_tiempo_cambio_direccion >= intervalo_cambio_direccion_bloque:
            direccion_bloque = random.choice(["arriba", "abajo", "izquierda", "derecha"])
            ultimo_tiempo_cambio_direccion = tiempo_actual_bloque
            intervalo_cambio_direccion_bloque = random.randint(1500, 2000)

        if direccion_bloque == "arriba":
            y_bloque -= velocidad_bloque
            if y_bloque < 0:
                y_bloque = 0
                direccion_bloque = "abajo"
        elif direccion_bloque == "abajo":
            y_bloque += velocidad_bloque
            if y_bloque > alto - tamano_bloque:
                y_bloque = alto - tamano_bloque
                direccion_bloque = "arriba"
        elif direccion_bloque == "izquierda":
            x_bloque -= velocidad_bloque
            if x_bloque < 0:
                x_bloque = 0
                direccion_bloque = "derecha"
        elif direccion_bloque == "derecha":
            x_bloque += velocidad_bloque
            if x_bloque > ancho - tamano_bloque:
                x_bloque = ancho - tamano_bloque
                direccion_bloque = "izquierda"

        # Movimiento en diagonal para bloques adicionales
        for bloque in bloques_adicionales:
            if bloque['direccion'] == "arriba_izquierda":
                bloque['x'] -= bloque['velocidad']
                bloque['y'] -= bloque['velocidad']
                if bloque['x'] < 0:
                    bloque['x'] = 0
                    bloque['direccion'] = "arriba_derecha"
                if bloque['y'] < 0:
                    bloque['y'] = 0
                    bloque['direccion'] = "abajo_izquierda"
            elif bloque['direccion'] == "arriba_derecha":
                bloque['x'] += bloque['velocidad']
                bloque['y'] -= bloque['velocidad']
                if bloque['x'] > ancho - tamano_bloque:
                    bloque['x'] = ancho - tamano_bloque
                    bloque['direccion'] = "arriba_izquierda"
                if bloque['y'] < 0:
                    bloque['y'] = 0
                    bloque['direccion'] = "abajo_derecha"
            elif bloque['direccion'] == "abajo_izquierda":
                bloque['x'] -= bloque['velocidad']
                bloque['y'] += bloque['velocidad']
                if bloque['x'] < 0:
                    bloque['x'] = 0
                    bloque['direccion'] = "abajo_derecha"
                if bloque['y'] > alto - tamano_bloque:
                    bloque['y'] = alto - tamano_bloque
                    bloque['direccion'] = "arriba_izquierda"
            elif bloque['direccion'] == "abajo_derecha":
                bloque['x'] += bloque['velocidad']
                bloque['y'] += bloque['velocidad']
                if bloque['x'] > ancho - tamano_bloque:
                    bloque['x'] = ancho - tamano_bloque
                    bloque['direccion'] = "abajo_izquierda"
                if bloque['y'] > alto - tamano_bloque:
                    bloque['y'] = alto - tamano_bloque
                    bloque['direccion'] = "arriba_derecha"

        for bloque in bloques_adicionales:
            if bloque['direccion'] == "arriba":
                bloque['y'] -= bloque['velocidad']
                if bloque['y'] < 0:
                    bloque['y'] = 0
                    bloque['direccion'] = "abajo"
            elif bloque['direccion'] == "abajo":
                bloque['y'] += bloque['velocidad']
                if bloque['y'] > alto - tamano_bloque:
                    bloque['y'] = alto - tamano_bloque
                    bloque['direccion'] = "arriba"
            elif bloque['direccion'] == "izquierda":
                bloque['x'] -= bloque['velocidad']
                if bloque['x'] < 0:
                    bloque['x'] = 0
                    bloque['direccion'] = "derecha"
            elif bloque['direccion'] == "derecha":
                bloque['x'] += bloque['velocidad']
                if bloque['x'] > ancho - tamano_bloque:
                    bloque['x'] = ancho - tamano_bloque
                    bloque['direccion'] = "izquierda"

        if tiempo_actual_bloque - ultimo_tiempo_bloque >= intervalo_bloque_adicional:
            if len(bloques_adicionales) < 9:
                nuevo_bloque = {
                    'x': random.randint(0, ancho - tamano_bloque),
                    'y': random.randint(0, alto - tamano_bloque),
                    'velocidad': 0.7,
                    'direccion': random.choice(["arriba", "abajo", "izquierda", "derecha"]),
                    'intervalo_cambio_direccion': random.randint(1500, 2000),
                    'ultimo_tiempo_cambio_direccion': pygame.time.get_ticks()
                }
                bloques_adicionales.append(nuevo_bloque)
                ultimo_tiempo_bloque = tiempo_actual_bloque

        colision = False
        for bloque in bloques_adicionales:
            if (x_cubo < bloque['x'] + tamano_bloque and x_cubo + tamano_cubo > bloque['x'] and
                    y_cubo < bloque['y'] + tamano_bloque and y_cubo + tamano_cubo > bloque['y']):
                colision = True
                break

        if (x_cubo < x_bloque + tamano_bloque and x_cubo + tamano_cubo > x_bloque and
                y_cubo < y_bloque + tamano_bloque and y_cubo + tamano_cubo > y_bloque) or colision:
            reiniciar_juego()
            inicio_tiempo = pygame.time.get_ticks()

        ventana.fill(color_fondo)
        ventana.blit(textura_bloque, (x_bloque, y_bloque))
        ventana.blit(textura_cubo_rojo, (x_cubo, y_cubo))

        for bloque in bloques_adicionales:
            ventana.blit(textura_bloque, (bloque['x'], bloque['y']))

        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - inicio_tiempo) // 1000
        texto_tiempo = fuente.render(f"Sobrevive: {tiempo_transcurrido} segundos", True, (255, 255, 255))
        rectangulo_tiempo = texto_tiempo.get_rect(center=(ancho // 2, 50))
        ventana.blit(texto_tiempo, rectangulo_tiempo)

        pygame.display.update()

    pygame.quit()

# Cargar imágenes de fondo
fondo_menu = pygame.image.load(r"Texturas/Menu de inicio.jpeg")
fondo_menu = pygame.transform.scale(fondo_menu, (ancho, alto))

fondo_juego = pygame.image.load(r"Texturas/Fondo.jpg")
fondo_juego = pygame.transform.scale(fondo_juego, (ancho, alto))

# Bucle principal
ejecutando = True
en_menu = True

fuente_menu = pygame.font.Font(None, 48)
texto_iniciar = fuente_menu.render("Iniciar", True, (255, 255, 255))
texto_salir = fuente_menu.render("Salir", True, (255, 255, 255))

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    if en_menu:
        if teclas[pygame.K_RETURN]:
            en_menu = False
            reiniciar_juego()
        elif teclas[pygame.K_q]:
            ejecutando = False

        pos_mouse = pygame.mouse.get_pos()
        click_mouse = pygame.mouse.get_pressed()

        rectangulo_texto_iniciar = texto_iniciar.get_rect(center=(ancho // 2, alto // 2 + 50))
        rectangulo_texto_salir = texto_salir.get_rect(center=(ancho // 2, alto // 2 + 150))

        if rectangulo_texto_iniciar.collidepoint(pos_mouse):
            texto_iniciar = fuente_menu.render("Iniciar", True, (255, 0, 0))
            if click_mouse[0] == 1:
                en_menu = False
                reiniciar_juego()

        if rectangulo_texto_salir.collidepoint(pos_mouse):
            texto_salir = fuente_menu.render("Salir", True, (255, 0, 0))
            if click_mouse[0] == 1:
                ejecutando = False

        ventana.fill(color_fondo)
        ventana.blit(fondo_menu, (0, 0))
        ventana.blit(texto_iniciar, rectangulo_texto_iniciar)
        ventana.blit(texto_salir, rectangulo_texto_salir)
    else:
        ventana.blit(fondo_juego, (0, 0))
        bucle_juego()

    pygame.display.update()

pygame.quit()
