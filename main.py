import pygame
import time
import random
# Display
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame IPGame")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
square = pygame.Surface((800, 200))
square.fill((7, 230, 119))
# Sound
sound = pygame.mixer.Sound('cong.mp3')
# Score
score = 0
missed_circles = 0
my_font = pygame.font.Font('Liter-Regular.ttf', 30)
# Lose condition
lose_label = my_font.render('You lost, try again!', False, (245, 0, 0))
# Victory condition
win_label = my_font.render('You won, level 2!', False, (7, 230, 52))
win_label_2 = my_font.render('You won, my congratulations!', False, (7, 230, 52))
# Restart
restart_label = my_font.render('Try again', False, (245, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(350, 300))


def update_score():
    return my_font.render(f"Score: {score}", False, (199, 38, 40))


def update_missed_circles():
    return my_font.render(f"Missed circles: {missed_circles}", False, (199, 38, 40))


text_surface = update_score()
pygame.display.update()
text_surface_1 = update_missed_circles()
pygame.display.update()

# PLayer
player = icon

player_speed = 5
player_x = 150
player_y = 429
walk_left = pygame.image.load('iconleft.png')
player_rect = player.get_rect(topleft=(player_x, player_y))

# Circle
circles = []
circle_radius = 25
circle_speed = 5
target_y = 450 - circle_radius

last_spawn_time = time.time()
spawn_interval = 3

gameplay = True
running = True
while running:
    pygame.time.delay(20)
    if gameplay:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            player = walk_left
        elif keys[pygame.K_RIGHT] and player_x < 505:
            player_x += player_speed
            player = icon

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if time.time() - last_spawn_time > spawn_interval:
            new_x = random.randint(circle_radius, 800 - circle_radius)
            circles.append([new_x, -1])
            last_spawn_time = time.time()

        for circle in circles:
            if circle[1] < target_y:
                circle[1] += circle_speed

        if len(circles) > 1:
            circles.pop(0)

        if len(circles) > 0:
            circle = circles[0]
            circle_rect = pygame.Rect(circle[0] - circle_radius, circle[1] - circle_radius - 1, circle_radius * 2,
                                    circle_radius * 2)
            player_rect = player.get_rect(topleft=(player_x, player_y))
            if player_rect.colliderect(circle_rect):
                score += 1
                text_surface = update_score()
                circles.pop(0)
                pygame.display.update()

            if len(circles) > 0:
                if circle[1] >= target_y and circle[1] < target_y + circle_radius:
                    missed_circles += 1
                    text_surface_1 = update_missed_circles()
                    circles.pop(0)
                    pygame.display.update()
        screen.fill((7, 171, 230))
        screen.blit(square, (0, 450))
        screen.blit(text_surface, (10, 570))
        screen.blit(player, (player_x, 300))
        screen.blit(text_surface_1, (300, 570))

# Boards
        if score == 10:
            gameplay = False
            screen.fill((7, 14, 230))
            screen.blit(win_label, (100, 200))
            pygame.display.update()
            time.sleep(2)
            circle_speed += 0.5
            circles.clear()
            last_spawn_time = time.time()

            score += 1

            screen.fill((7, 171, 230))
            screen.blit(square, (0, 450))
            screen.blit(update_score(), (10, 570))
            screen.blit(update_missed_circles(), (300, 570))
            screen.blit(player, (player_x, 300))

            pygame.display.update()

            gameplay = True

        if score == 20:
            screen.fill((7, 14, 230))
            screen.blit(win_label_2, (100, 200))
            gameplay = False
            sound.play()
            pygame.display.update()

        elif missed_circles == 3:
            gameplay = False
            screen.fill('GRAY')
            screen.blit(lose_label, (300, 200))
            screen.blit(restart_label, restart_label_rect)
            pygame.display.update()

    for circle in circles:
        pygame.draw.circle(screen, (199, 38, 40), (circle[0], circle[1]), circle_radius)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_label_rect.collidepoint(event.pos) and not gameplay:
                score = 0
                missed_circles = 0
                circles = []
                player_x = 150
                gameplay = True
                screen.fill((7, 171, 230))
                text_surface = update_score()
                text_surface_1 = update_missed_circles()
                pygame.display.update()
