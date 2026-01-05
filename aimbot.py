"""
“This aim trainer challenges players to click moving targets under time pressure 
while avoiding bombs. Each round increases difficulty until the player fails.”
"""

# imports
import pygame 
import time
import random

from pygame.time import Clock

# constants
TIME_PER_ROUND = 10000
MIN_TIME = 5000


WIDTH = 600
HEIGHT = 800
SPEED = 2
RADIUS = 40
MIN_RADIUS = 20 
MAX_RADIUS = min(WIDTH, HEIGHT) // 4


# helper functions to check the time 
def current_time():
    return int(time.time() * 1000)





def remaining_time():
    return round((future - current_time()) / 1000)

# pygame and color setup 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Practice Game")
font = pygame.font.Font('freesansbold.ttf', 32)
clock = Clock()


GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

# adds taregt and bomb circles to a list (these are just the starting values of position, radius, and number of each type of circle)
def fill_list(num_targets=5, num_bombs=3, target_radius=40, bomb_radius=40):
    circles = []
    for _ in range(num_targets):
        circle = {
            "x": random.randint(target_radius, WIDTH-target_radius),
            "y": random.randint(target_radius, HEIGHT- target_radius),
            "dx": random.choice([-3, -2, 2, 3]),
            "dy": random.choice([-3, -2, 2, 3]),
            "radius": target_radius,
            "color": GREEN,
            "type": "target"
        }
        circles.append(circle)

    for _ in range(num_bombs):
        circle = {
            "x": random.randint(bomb_radius, WIDTH- bomb_radius),
            "y": random.randint(bomb_radius, HEIGHT-bomb_radius),
            "dx": random.choice([-3, -2, 2, 3]),
            "dy": random.choice([-3, -2, 2, 3]),
            "radius": bomb_radius,
            "color": RED,
            "type": "bomb"
        }
        circles.append(circle)
    return circles

# uses the velocity of each circle to make it move automatically and bounce of walls if the circle hits the wall 
def move(circles):
    for circle in circles: 
        circle["x"] += circle["dx"]
        circle["y"] += circle["dy"]

            # Bounce off walls
        if circle["x"] - circle["radius"] <= 0 or circle["x"] + circle["radius"] >= WIDTH:
            circle["dx"] *= -1
        if circle["y"] - circle["radius"] <= 0 or circle["y"] + circle["radius"] >= HEIGHT:
            circle["dy"] *= -1

# draws the circles onto the screen
def draw(circles):
    for circle in circles:
        pygame.draw.circle(screen, circle["color"], (circle["x"], circle["y"]), circle["radius"])


# checks how many targets are on the screen at any point 
def check_total(circles):
    count = 0 
    for circle in circles: 
        if circle["type"] == "target":
            count += 1
    return count  
# handles the win lose situations allowing it to move onto the next round or not 
def handle_round(circles):
    total = check_total(circles)


    if remaining_time() <= 0 and total > 0: 
        return "lose"
    if total == 0: 
        return "win"
    
    return "continue"

# scale factors to increase the difficultly of each upcoming round 
def difficulty_scaling(round_number):
    round_time = max(TIME_PER_ROUND- round_number * 500, MIN_TIME)
    target_radius_this_round = max(RADIUS - round_number * 2, MIN_RADIUS)
    bomb_radius_this_round = min(RADIUS + round_number * 2, MAX_RADIUS)
    num_targets = min(5 + round_number // 2, 9)
    num_bombs = min(3 + round_number // 3, 5)



    return num_targets, num_bombs, target_radius_this_round, bomb_radius_this_round, round_time
    

# start of the game loop 
running = True
score = 0
round_number = 1
future = current_time() + TIME_PER_ROUND
filled_list = fill_list()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        # checks if user leaves the game 
        if event.type == pygame.QUIT:
            running = False
            # checks what the user clicks with the mouse, if target the target is removed from the screen and list 
            # it also adds a point for the user
            # if bomb the game ends 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            for circle in filled_list:
                dist = ((mx - circle["x"])**2  + (my - circle["y"])**2)**0.5
                if dist <= circle["radius"]:
                    if circle["type"] == "target":
                        score += 1
                        
                        filled_list.remove(circle)
                        total = check_total(filled_list)
                        break
                    elif circle["type"] == "bomb":
                        running = False
                        print("You lost! You hit a bomb!")
                        print(f"Final score: {score}")

         

    
    # this sets the screen color and shows the round time and and score 
    screen.fill(CYAN)

    round_text = font.render(f"Round: {round_number}", True, BLACK, CYAN)
    round_rect = round_text.get_rect(center=(100, 20))
    time_text = font.render(f"Time Left: {remaining_time()}", True, BLACK, CYAN)
    time_rect = time_text.get_rect(center=(100, 50))
    score_text = font.render(f"Score: {score}", True, BLACK, CYAN)
    score_rect = score_text.get_rect(center=(100, 80))

    screen.blit(round_text, round_rect)
    screen.blit(time_text, time_rect)
    screen.blit(score_text, score_rect)
    # this draws and moves the circles on the screen
    draw(filled_list)
    move(filled_list)
    # handles win loss situations 
    round_status = handle_round(filled_list)
    # if loss the game is over 
    if round_status == "lose":
        running = False
        print(f"Time ran out! Final score: {score}")

    # if win, new round is started and difficulty factors are applied 
    if round_status == "win":
        round_number += 1
        num_targets, num_bombs, target_radius_this_round, bomb_radius_this_round, round_time = difficulty_scaling(round_number) 
        filled_list = fill_list(num_targets, num_bombs, target_radius_this_round, bomb_radius_this_round)
        future = current_time() + round_time
    # updates the screen
    pygame.display.flip()


# end of the game loop 
pygame.quit()