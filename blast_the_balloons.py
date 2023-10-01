import pygame
import random
import sys
import time 

## Screen parameters

width = 800
height = 600

# Colors 

RED = (255, 0, 0) # RGB --> RED, GREEN and BLUE (0-255, 0-255, 0-255)
LIGHT_GREY = (225, 225, 225)
LIGHT_GREY_2 = (220, 220, 220)
VIOLET = (148, 0, 211)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 225)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
WHITE = (255, 255, 255)

colors_list = [RED, VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE] # Giving Random to ballon

#Game Initialization variables

running = True
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blast The Balloon")

# Font sizes
font_size = 30
initial_screen_font_size = 40
font = pygame.font.Font(None, font_size)
initial_screen_font = pygame.font.Font(None, initial_screen_font_size)

# Start and end variables
start = False
start_text_pos_x, start_text_pos_y = (width // 2) - initial_screen_font_size, height // 2
end_text_pos_x, end_text_pos_y = (width // 2) - initial_screen_font_size, height // 2 + initial_screen_font_size

# Speed Control variables
interval = 800
last_interval = 0

# Cicles 
circles = [] # --> (radius, (x, y), colorslist) --> 
circle_radius = 20

# Scores and lives 
score = 0
lives = 5
score_pos_x = width - (4.8 * font_size)
score_pos_y = 20

lives_pos_x, lives_pos_y = width - (4.8 * font_size), score_pos_y + 28

# highscore
highscore = 0
highscore_pos_x, highscore_pos_y = width - (4.8 * font_size), score_pos_y + 56

# Area for displaying circles

circle_display_area_x1 = 100
circle_display_area_x2 = width - circle_display_area_x1

circle_display_area_y1 = 100
circle_display_area_y2 = height - circle_display_area_y1

# Btns

start_btn_width = 90
start_btn_height = 35
start_btn_x = (width - start_btn_width) // 2 - 13
start_btn_y = (height - start_btn_height) // 2 + 10

quit_btn_width = 90
quit_btn_height = 35
quit_btn_x = (width - start_btn_width) // 2 - 13
quit_btn_y = (height - start_btn_height) // 2 + 1.5 * quit_btn_height


while running:
    screen.fill(WHITE)
    score_text = font.render("Score: " + str(score), True, RED)
    lives_text = font.render("Lives: " + str(lives), True, RED)
    highscore_text = font.render("Highscore: " + str(highscore), True, RED)
    current_time = pygame.time.get_ticks()
    if start == True:
        screen.blit(score_text, (score_pos_x, score_pos_y))
        screen.blit(lives_text, (lives_pos_x, lives_pos_y))
        screen.blit(highscore_text, (highscore_pos_x, highscore_pos_y))
        if current_time - last_interval >= interval:
            circle_x = random.randint(circle_display_area_x1, circle_display_area_x2) # 100 - 700
            circle_y = random.randint(circle_display_area_y1, circle_display_area_y2) # 100 - 600
            circles.append((circle_x, circle_y, random.choice(colors_list)))
        # pygame.draw.circle(screen, random.choice(colors_list), (random.randint(50, width - 20), random.randint(50, height - 20)), circle_radius)
            last_interval = current_time

        for circle in circles:
            pygame.draw.circle(screen, circle[2], (circle[0], circle[1]), circle_radius)
        
        if len(circles) == 2:
            circles.pop(0)
    else:
        start_text = initial_screen_font.render("Start", True, RED)
        end_text = initial_screen_font.render("End", True, RED)

        pygame.draw.rect(screen, LIGHT_GREY, (start_btn_x, start_btn_y, start_btn_width, start_btn_height))

        pygame.draw.rect(screen, LIGHT_GREY, (quit_btn_x, quit_btn_y, quit_btn_width, quit_btn_height))

        screen.blit(start_text, (start_text_pos_x, start_text_pos_y))
        screen.blit(end_text, (end_text_pos_x, end_text_pos_y))
        screen.blit(score_text, (score_pos_x, score_pos_y))
        screen.blit(lives_text, (lives_pos_x, lives_pos_y))
        screen.blit(highscore_text, (highscore_pos_x, highscore_pos_y))



    # print(circles)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cur_x, cur_y = pygame.mouse.get_pos()

            if len(circles) == 1:
                cur_circle_x, cur_circle_y = circles[0][0], circles[0][1]
                if start == True and ((abs(cur_circle_x - cur_x) <= circle_radius) and (abs(cur_circle_y - cur_y) <= circle_radius)):
                    pygame.mixer_music.load("balloon_pop_sound.mp3")
                    pygame.mixer_music.play()
                    score += 1
                elif start == True:
                    lives -= 1

            if start == False and ((abs(start_btn_x - cur_x) <= start_btn_width) and (abs(start_btn_y - cur_y) <= start_btn_height)):
                start = True
            elif start == False and ((abs(quit_btn_x - cur_x) <= quit_btn_width) and (abs(quit_btn_y - cur_y) <= quit_btn_height)):
                running = False


    if lives == 0:
        pygame.mixer_music.load("game_over_sound.mp3")
        pygame.mixer_music.play()
        lives = 5
        highscore = max(score, highscore)
        score = 0
        start = False

    pygame.display.flip()

pygame.quit()
sys.exit()