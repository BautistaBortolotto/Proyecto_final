import pygame
import random
import sys
#Importo librerias

pygame.init()

width = 800
height = 600

screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h

background_color = (0, 0, 0, 0)

window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Cube adventure")

icon_image = pygame.image.load(r"Texturas\alien.png")
pygame.display.set_icon(icon_image)

rect_size = 100
rect_x = width // 2 - rect_size // 2
rect_y = height - rect_size
rect_speed = 1

block_size = 150
block_x = random.randint(0, width - block_size)
block_y = random.randint(0, height - block_size)
block_speed = 0.7

font = pygame.font.Font(None, 36)
counter = 0
start_time = pygame.time.get_ticks()

last_time_counter = pygame.time.get_ticks()
last_time_block = pygame.time.get_ticks()
block_speed_increase_interval = 60000
additional_block_interval = 30000

block_direction = random.choice(["up", "down", "left", "right"])
block_direction_change_interval = random.randint(1500, 2000)
last_time_direction_change = pygame.time.get_ticks()

additional_blocks = []

red_square_texture = pygame.image.load(r"Texturas\alien.png").convert_alpha()
red_square_texture = pygame.transform.scale(red_square_texture, (rect_size, rect_size))

music = pygame.mixer.Sound(r"Audios\Musicaparacubocubico.mp3")
music.play(-1)

def reset_game():
    global rect_x, rect_y, counter, last_time_counter, last_time_block, last_time_direction_change
    rect_x = width // 2 - rect_size // 2
    rect_y = height - rect_size
    counter = 0
    last_time_counter = pygame.time.get_ticks()
    last_time_block = pygame.time.get_ticks()
    last_time_direction_change = pygame.time.get_ticks()
    additional_blocks.clear()

texture_image = pygame.image.load(r"Texturas\piedra con graficasos.png").convert_alpha()
texture_image = pygame.transform.scale(texture_image, (block_size, block_size))

background_image = pygame.image.load(r"Texturas\Fondo.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (width, height))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and rect_y > 0:
        rect_y -= rect_speed
    if keys[pygame.K_s] and rect_y < height - rect_size:
        rect_y += rect_speed
    if keys[pygame.K_a] and rect_x > 0:
        rect_x -= rect_speed
    if keys[pygame.K_d] and rect_x < width - rect_size:
        rect_x += rect_speed

    current_time_counter = pygame.time.get_ticks()
    if current_time_counter - last_time_counter >= 1000:
        counter += 1
        last_time_counter = current_time_counter

    current_time_block = pygame.time.get_ticks()
    if current_time_block - last_time_block >= block_speed_increase_interval:
        block_speed += 0.1
        last_time_block = current_time_block

    if current_time_block - last_time_direction_change >= block_direction_change_interval:
        block_direction = random.choice(["up", "down", "left", "right"])
        last_time_direction_change = current_time_block
        block_direction_change_interval = random.randint(1500, 2000)

    if block_direction == "up":
        block_y -= block_speed
        if block_y < 0:
            block_y = 0
            block_direction = "down"
    elif block_direction == "down":
        block_y += block_speed
        if block_y > height - block_size:
            block_y = height - block_size
            block_direction = "up"
    elif block_direction == "left":
        block_x -= block_speed
        if block_x < 0:
            block_x = 0
            block_direction = "right"
    elif block_direction == "right":
        block_x += block_speed
        if block_x > width - block_size:
            block_x = width - block_size
            block_direction = "left"

    for block in additional_blocks:
        if block['direction'] == "up":
            block['y'] -= block['speed']
            if block['y'] < 0:
                block['y'] = 0
                block['direction'] = "down"
        elif block['direction'] == "down":
            block['y'] += block['speed']
            if block['y'] > height - block_size:
                block['y'] = height - block_size
                block['direction'] = "up"
        elif block['direction'] == "left":
            block['x'] -= block['speed']
            if block['x'] < 0:
                block['x'] = 0
                block['direction'] = "right"
        elif block['direction'] == "right":
            block['x'] += block['speed']
            if block['x'] > width - block_size:
                block['x'] = width - block_size
                block['direction'] = "left"

    if current_time_block - last_time_block >= additional_block_interval:
        if len(additional_blocks) < 9:
            new_block = {
                'x': random.randint(0, width - block_size),
                'y': random.randint(0, height - block_size),
                'speed': 0.7,
                'direction': random.choice(["up", "down", "left", "right"]),
                'direction_change_interval': random.randint(1500, 2000),
                'last_time_direction_change': pygame.time.get_ticks()
            }
            additional_blocks.append(new_block)
            last_time_block = current_time_block

    collision = False
    for block in additional_blocks:
        if (rect_x < block['x'] + block_size and rect_x + rect_size > block['x'] and
                rect_y < block['y'] + block_size and rect_y + rect_size > block['y']):
            collision = True
            break

    if (rect_x < block_x + block_size and rect_x + rect_size > block_x and
            rect_y < block_y + block_size and rect_y + rect_size > block_y) or collision:
        reset_game()
        start_time = pygame.time.get_ticks()

    window.blit(background_image, (0, 0))
    window.blit(texture_image, (block_x, block_y))
    window.blit(red_square_texture, (rect_x, rect_y))

    for block in additional_blocks:
        window.blit(texture_image, (block['x'], block['y']))


    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    time_text = font.render(f"Sobrevive: {elapsed_time} segundos", True, (255, 255, 255))
    time_rect = time_text.get_rect(center=(width // 2, 50))
    window.blit(time_text, time_rect)

    pygame.display.update()

pygame.quit()
