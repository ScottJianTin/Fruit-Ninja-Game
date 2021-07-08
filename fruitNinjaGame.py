import pygame
import sys
import os
import random

# Initialize window
player_lives = 3
score = 0
fruits = ["melon", "orange", "pomegranate", "guava", "bomb"]
width = 800
height = 500
fps = 12

pygame.init()
pygame.display.set_caption("FRUIT NINJA")
game_display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

game_display.fill((black))
background = pygame.image.load("back.jpg")
font = pygame.font.Font(os.path.join(os.getcwd(), "comic.ttf"), 32)
score_text = font.render("Score : " + str(score), True, (255, 255, 255))
lives_icon = pygame.image.load("images/white_lives.png")

# Define functions


def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        "img": pygame.image.load(fruit_path),
        "x": random.randint(100, 500),
        "y": 800,
        "speed_x": random.randint(-10, 10),
        "speed_y": random.randint(-80, -60),
        "throw": False,
        "t": 0,
        "hit": False
    }

    if random.random() >= 0.75:
        data[fruit]["throw"] = True
    else:
        data[fruit]["throw"] = False


data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

# Draw fonts
font_name = pygame.font.match_font("comic.ttf")


def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    game_display.blit(text_surface, text_rect)

# Draw player lives


def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)


def hide_cross_lives(x, y):
    game_display.blit(pygame.image.load("images/red_lives.png"), (x, y))

# Game over display & front display


def show_gameover_screen():
    game_display.blit(background, (0, 0))
    draw_text(game_display, "FRUIT NINJA!", 64, width/2, height/4)
    if not game_over:
        draw_text(game_display, "Score:" + str(score), 40, width/2, 250)

    draw_text(game_display, "Press a key to begin!", 24, width/2, height*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# Game loop
first_round = True
game_over = True
game_running = True
while game_running:
    if game_over:
        if first_round:
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(game_display, 690, 5, player_lives, "images/red_lives.png")
        score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    game_display.blit(background, (0, 0))
    game_display.blit(score_text, (0, 0))
    draw_lives(game_display, 690, 5, player_lives, "images/red_lives.png")

    for key, value in data.items():
        if value["throw"]:
            value["x"] += value["speed_x"]
            value["y"] += value["speed_y"]
            value["speed_y"] += (1 * value["t"])
            value["t"] += 1

            if value["y"] <= 800:
                game_display.blit(value["img"], (value["x"], value["y"]))
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()

            if not value["hit"] and current_position[0] > value["x"] and current_position[0] < value["x"]+60 and current_position[1] > value["y"] and current_position[1] < value["y"]+60:
                if key == "bomb":
                    player_lives -= 1
                    if player_lives == 0:
                        hide_cross_lives(690, 15)
                    elif player_lives == 1:
                        hide_cross_lives(725, 15)
                    elif player_lives == 2:
                        hide_cross_lives(760, 15)

                    if player_lives < 0:
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "images/explosion.png"

                else:
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value["img"] = pygame.image.load(half_fruit_path)
                value["speed_x"] += 10
                if key != "bomb":
                    score += 1
                score_text = font.render(
                    "Score : " + str(score), True, (255, 255, 255))
                value["hit"] = True

        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
