import pygame
import math

#Setup
pygame.init()
screen = pygame.display.set_mode((1920,1080)) #Set resolution for screen. Don't change this value as it will mess things up.
clock = pygame.time.Clock() #Instaciates clock for the application.
running = True #While true the app will run and when false the app will close.
paused = False #Allows sim to be paused.
debug = False #Shows some visual debug stuff. Helps me visualize things to make it easier.
statText = pygame.font.SysFont('arial', 30) #Text Settings for all of the text displayed.

#Physics variables
gravity = 0.6 #Default is 0.6, Isn't finely tuned so this will likely change.
speed = pygame.Vector2(20, -5) #Speed of ball and the direction +x is right -x is left, +y is down -y is upwards. This is because the coordinate system starts at the top left.
speedAngle = 0 #Gets angle of speed.
angle = 0 #Angle of the balls from the center of the circle, 0 - 359.
center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) #Center of screen, used for finding ball relative to the center containing circle.


#maxSpeed = 100 max speed for ball if wanted. Currently not implemented.
collided = False #Stops ball from bouncing more than once while colliding.
radius = 500 #Radius of the containing circle. Can be freely changed but I would recommend to leave as is.
energyLoss = 0.95 #lost energy on bounce, numbers less than 1 cause it to lose energy on bounce and numbers greater than one cause it to gain energy.
waitDefault = 2 #Default value for wait, recommended to leave at 2.
wait = 2 #Frames to wait before turning off collided, Stops the ball from being stuck in the wall.
top = pygame.Vector2(screen.get_width() / 2, (screen.get_height() / 2) - radius) #Top of incasing circle, used for calculations.

#Physics objects
ballCoords = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) #Ball coords on screen with [0,0] being top left.
centeredCoords = pygame.Vector2(0, 0) #Ball coordinates which are centered to the screen. Allows for easier calculations.

while running:
    #Events
    for event in pygame.event.get(): #Quit app when Quit putton is pressed
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: #Pause Sim when p key is pressed.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                paused = not paused
            elif keys[pygame.K_d]:
                debug = not debug
    
    if not paused:
        #Math
        ballDistance = ballCoords.distance_to(center) #Get ball's distance from center, Used for angle calculations and collisions.

        #Gets the angle around the center point, 0 - 359.
        sideC = ballDistance
        sideB = radius
        sideA = ballCoords.distance_to(top)

        if centeredCoords.x == 0:
            if -centeredCoords.y <= 0:
                angle = 180
            else:
                angle = 0
        elif -centeredCoords.y == 0:
            if centeredCoords.x <= 0:
                angle = 270
            else:
                angle = 90
        elif -centeredCoords.y == 0 and centeredCoords.x == 0:
            angle = 0
        else:
            '''
            A little explanation of how I get this angle.
            Uses 3 sides to find the angle, SideA being the balls distance from the top of the circle, 
            SideB being the radius of the circle, and SideC which is the balls distance from the center of the circle.
            Using these variables we can plug them into the law of cosine function which returns us the angle, 
            Then if its on the left side of the circle we subtract the angle from 360 to get the correct angle.
            '''
            angle = math.degrees(math.acos(((sideB * sideB) + (sideC * sideC) - (sideA * sideA))/(2 * sideB * sideC)))
            if centeredCoords.x < 0:
                angle = 360 - angle
        
        #Get angle of speed
        
        speedAngle = 1 #I'm being dumb and was doing this way wrong

            

        #Calculate gravity and if colliding.
        #Bounces are not correct yet.
        colliding = ballDistance >= radius
        
        if colliding and not collided:
            collided = True
            speed *= -energyLoss
        elif collided:
            if wait == 0:
                wait = waitDefault
                collided = False
            else:
                wait -= 1
        
        ballCoords += speed
        speed.y += gravity

        #Fill screen
        screen.fill("black")

        #Render Frames
        #Render Circles and debug line
        
        pygame.draw.circle(screen, "white", center, radius+5)
        pygame.draw.circle(screen, "black", center, radius)
        if debug:
            pygame.draw.line(screen, "yellow", center, ballCoords, 3)
            pygame.draw.line(screen, "orange", center, top)
            pygame.draw.line(screen, "orange", top, ballCoords)
            pygame.draw.circle(screen, "red", center, 4)
            pygame.draw.line(screen, "Blue", ballCoords, (ballCoords.x, ballCoords.y + 4 * speed.y), 5)
            pygame.draw.line(screen, "Red", ballCoords, (ballCoords.x + 4 * speed.x, ballCoords.y), 5)
        pygame.draw.circle(screen, "white", ballCoords, 5)

        

        #Render Text
        
        centeredCoords = ballCoords - center #Centered coords for position.

        speedSurface = statText.render(f"Speed: {round(speedAngle, 2)} {round(speed, 2)}", False, 'White')
        positionSurface = statText.render(f"Position: [{round(centeredCoords.x, 2)}, {round(-centeredCoords.y, 2)}]", False, 'White')
        angleSurface = statText.render(f"Angle: {round(angle, 2)}", False, 'White')    
        sideSurface = statText.render(f"SideA: {round(sideA)} SideB: 500 SideC: {round(sideC)}", False, 'white')
        screen.blit(speedSurface, (screen.get_width() / 1.3, screen.get_height() / 6))
        screen.blit(positionSurface, (screen.get_width() / 1.3, screen.get_height() / 5))
        screen.blit(angleSurface, (screen.get_width() / 1.3, screen.get_height() / 4.3))
        screen.blit(sideSurface, (screen.get_width() / 1.5, screen.get_height() - 100))

    #Flip to send frame
    pygame.display.flip()

    clock.tick(60) #Frames per second but it will mess with sim if changed so leave it as is, I may change this sometime.

pygame.quit