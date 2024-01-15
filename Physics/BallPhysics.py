import pygame
import math

#Setup
pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
running = True
statText = pygame.font.SysFont('arial', 30)

#Physics variables
gravity = 0.6 #Default is 0.6, Isn't finely tuned so this will likely change
speed = pygame.Vector2(10, -10) #Speed of ball and the direction +x is right, +y is down
angle = 0 #Angle of the balls speed 0 - 360, 0 being directly upwards and angle and is clockwise
center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) #Center of screen, used for finding ball relative to the containing circle

#maxSpeed = 100 max speed for ball if wanted
collided = False #Stops ball from bouncing more than once while colliding once
radius = 500 #Radius of the containing circle
energyLoss = 0.1 #lost energy on bounce, is 1.00 - 0.00, can be over 1 to make it gain energy
waitDefault = 3 #Default value for wait
wait = 3 #Frames to wait before turning off collided, Stops the ball from being stuck in the wall

#Physics objects
ballCoords = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) #Ball coords on screen with [0,0] being top left

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
    speedSurface = statText.render(f"Speed: {round(math.sqrt((speed.x * speed.x) + (speed.y * speed.y)), 5)} {speed}", False, 'White')
    positionSurface = statText.render(f"Position: {ballCoords}", False, 'White')
    angleSurface = statText.render(f"Angle: {angle}", False, 'White')
    screen.blit(speedSurface, (screen.get_width() / 1.2, screen.get_height() / 6))
    screen.blit(positionSurface, (screen.get_width() / 1.2, screen.get_height() / 5))
    screen.blit(angleSurface, (screen.get_width() / 1.2, screen.get_height() / 4.3))

    #Flip to send frame
    pygame.display.flip()

    #Math for next frame
    #Get Hypotenuse
    hyp = math.sqrt(((ballCoords.x - center.x) * (ballCoords.x - center.x)) + ((ballCoords.y - center.y) * (ballCoords.y - center.y)))

    #Get Angle (I want to find a easier way to do this but it errors if either value is 0 so the if checks stay for now)
    if speed.x == 0:
        if -speed.y <= 0:
            angle = 180
        else:
            angle = 0
    elif -speed.y == 0:
        if speed.x <= 0:
            angle = 270
        else:
            angle = 90
    else:
        angle = math.tan(speed.y/speed.x)

    #Calculate gravity and if colliding
    
    colliding = hyp >= radius

    if colliding and not collided:
        collided = True
        speed *= -1 #Not at all correct bounces but I needed something simple to test collisions, Collisions aren't perfect but they'll work for now
    elif collided:
        if wait == 0:
            wait = waitDefault
            collided = False
        else:
            wait -= 1
    speed.y += gravity
    ballCoords += speed


    clock.tick(60) #Frames per second but it will mess with sim if changed so leave it as is, I may change this sometime

pygame.quit