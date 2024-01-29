import pygame
import math

#Setup
pygame.init()
screen = pygame.display.set_mode((1920,1080)) #Set resolution for screen. Don't change this value as it will mess things up.
clock = pygame.time.Clock()
running = True #While true the app will run and when false the app will close.
paused = False #Allows sim to be paused.
debug = False #Shows some visual debug stuff. Helps me visualize things to make it easier.
statText = pygame.font.SysFont('arial', 30)

#Physics variables
gravity = 0.6 #Default is 0.6, Isn't finely tuned so this will likely change.
speed = pygame.Vector2(20, -5) #Speed of ball and the direction +x is right -x is left, +y is down -y is upwards. This is because the coordinate system starts at the top left.
speedAngle = 0 #Gets angle of speed.
angle = 0 #Angle of the balls from the center of the circle, 0 - 359.
center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) #Center of screen, used for finding ball relative to the center containing circle.
radius = 500 #Radius of the containing circle. Can be freely changed but I would recommend to leave as is.
energyLoss = 0.95 #lost energy on bounce, numbers less than 1 cause it to lose energy on bounce and numbers greater than one cause it to gain energy.
collided = False #Stops ball from bouncing more than once while colliding.
waitDefault = 2 #Default value for wait, recommended to leave at 2.
wait = 2 #Frames to wait before turning off collided.
top = pygame.Vector2(screen.get_width() / 2, (screen.get_height() / 2) - radius) #Top of containing circle, used for calculations.
collisionPoint = pygame.Vector2(0,0) #Point of collision. Used to stop ball from going through container.

#Physics objects
ballCoords = pygame.Vector2(center) #Ball coords on screen with [0,0] being top left.
centeredCoords = pygame.Vector2(0, 0) #Ball coordinates which are centered to the screen. Allows for easier calculations.

while running:
    #Events
    for event in pygame.event.get(): #Quit app when Quit putton is pressed
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]: #Pause Sim when p key is pressed.
                paused = not paused
            elif keys[pygame.K_d]: #Enable debug mode.
                debug = not debug
    
    if not paused:
    

        #Math
        ballDistance = ballCoords.distance_to(center) #Get ball's distance from center, Used for angle calculations and collisions.
        centeredCoords = ballCoords - center #Centered coords for position.
        speedAngle = 1 #Angle of speed
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
            If debug is enabled this is shown by the orange triangle.
            '''
            angle = math.degrees(math.acos(((sideB ** 2) + (sideC ** 2) - (sideA ** 2))/(2 * sideB * sideC)))
            if centeredCoords.x < 0:
                angle = 360 - angle

        #Get collision point
        

        if ballDistance > 500: #stop ball from passing throught the container
            collisionPoint = [1,1] #unsure how to do this atm.

        #Calculate gravity and if colliding.
        #Bounces are not correct yet.
        colliding = ballDistance >= radius
        ballCoords += speed
        speed.y += gravity
        if colliding and not collided:
            collided = True
            #paused = True
            speed *= -energyLoss
        elif collided:
            if wait == 0:
                wait = waitDefault
                collided = False
            else:
                wait -= 1
        
        
            
        

        #Fill screen
        screen.fill("black")

        #Render Frames
        #Render Circles and debug line
        
        pygame.draw.circle(screen, "white", center, radius+5, 5)
        if debug:
            pygame.draw.line(screen, "orange", center, ballCoords)
            pygame.draw.line(screen, "orange", center, top)
            pygame.draw.line(screen, "orange", top, ballCoords)
            pygame.draw.circle(screen, "red", center, 4)
            pygame.draw.line(screen, "Blue", ballCoords, (ballCoords.x, ballCoords.y + 4 * speed.y), 5)
            pygame.draw.line(screen, "Red", ballCoords, (ballCoords.x + 4 * speed.x, ballCoords.y), 5)

            #Render Text
            speedSurface = statText.render(f"Speed: {round(speedAngle, 2)} {round(speed, 2)}", False, 'White')
            positionSurface = statText.render(f"Position: [{round(centeredCoords.x, 2)}, {round(-centeredCoords.y, 2)}]", False, 'White')
            angleSurface = statText.render(f"Angle: {round(angle, 2)}", False, 'White')    
            sideSurface = statText.render(f"SideA: {round(sideA)} SideB: 500 SideC: {round(sideC)}", False, 'white')
            screen.blit(speedSurface, (screen.get_width() / 1.3, screen.get_height() / 6))
            screen.blit(positionSurface, (screen.get_width() / 1.3, screen.get_height() / 5))
            screen.blit(angleSurface, (screen.get_width() / 1.3, screen.get_height() / 4.3))
            screen.blit(sideSurface, (screen.get_width() / 1.5, screen.get_height() - 100))

        pygame.draw.circle(screen, "aqua", ballCoords, 5)

    #Flip to send frame
    pygame.display.flip()

    clock.tick(60) #Frames per second but it will mess with sim if changed so leave it as is.

pygame.quit