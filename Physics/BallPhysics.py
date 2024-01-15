import pygame
import math

#Setup
pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
running = True
statText = pygame.font.SysFont('arial', 30)

#Physics variables
gravity = 0.6 #Default is 9.81 but it may change if the sim is weird
speed = pygame.Vector2(0, 0) #Speed of ball and the direction

#maxSpeed = 100 max speed for ball if wanted

radius = 500 #Radius of the containing circle
colliding = False #Variable is true when colliding so we move to calculating collisions and bounce angles
energyLoss = 0.1 #lost energy on bounce, is a percentage 1.00 - 0.00, can be over 1 to make it gain energy



#Physics objects
ballCoords = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ballCoords.x = pygame.math.clamp(ballCoords.x, -100, 100) #(screen.get_width() / 2) - radius, (screen.get_width() / 2) + radius
ballCoords.y = pygame.math.clamp(ballCoords.y, -100, 100) #(screen.get_height() / 2) - radius, (screen.get_height() / 2) + radius

while running:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill screen
    screen.fill("black")

    #Render Frames
    #Render Circles
    pygame.draw.circle(screen, "white", pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), radius+5)
    pygame.draw.circle(screen, "black", pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), radius)
    pygame.draw.circle(screen, "white", ballCoords, 5)

    #Render Text
    speedSurface = statText.render(f"Speed: {round(math.sqrt((speed.x * speed.x) + (speed.y * speed.y)), 5)}", False, 'White')
    positionSurface = statText.render(f"Position: {ballCoords}", False, 'White')
    screen.blit(speedSurface, (screen.get_width() / 1.2, screen.get_height() / 6))
    screen.blit(positionSurface, (screen.get_width() / 1.2, screen.get_height() / 5))

    #Flip to send frame
    pygame.display.flip()

    #Math for next frame
    #Calculate gravity and bounces
    speed.y += gravity
    ballCoords += speed
    colliding = math.sqrt((ballCoords.x * ballCoords.x) + (ballCoords.y * ballCoords.y)) <= radius
    if colliding:
        speed.x = speed.x * -1
        speed.y = speed.y * -1


    clock.tick(60)

pygame.quit