import pygame
import math

#Setup
pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
running = True

#Physics variables
gravity = 0.6 #Default is 9.81 but it may change if the sim is weird
speed = pygame.Vector2(0, 0) #Speed of ball and the direction
#maxSpeed = 100 max speed for ball if wanted
radius = 500 #Radius of the containing circle
colliding = False #Variable is true when colliding so we move to calculating collisions and bounce angles

#Physics objects
ballCoords = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


while running:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill screen
    screen.fill("black")

    #Render frame
    pygame.draw.circle(screen, "white", pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), radius+5)
    pygame.draw.circle(screen, "black", pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), radius)
    pygame.draw.circle(screen, "white", ballCoords, 5)


    #Flip to send frame
    pygame.display.flip()

    #Math for next frame
    #Calculate gravity and bounces
    speed.y += gravity
    ballCoords += speed
    if math.sqrt((ballCoords.x * ballCoords.x) + (ballCoords.y * ballCoords.y)) >= radius:
        colliding = True
    #if colliding:
        #Collision math, Unsure how to do quite yet



    clock.tick(60)

pygame.quit