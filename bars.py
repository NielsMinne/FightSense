import pygame

#position and width for image 
BACKGROUND_BAR = [113, 647, 335, 20]

class Bar():
    def __init__(self, x, y,bar_width,bar_height):
        self.rect = pygame.Rect(x, y, bar_width, bar_height)
        self.speed = 1

    #def for moving the yellow bars (randomly 0-6)
    def move(self,surface,randomMove):
        dx = 0
        if randomMove == 0:
            dx =  -self.speed  * 3   
        elif randomMove == 1:
            dx = -self.speed * 2
        elif randomMove == 2:
            dx =  -self.speed * 1
        elif randomMove == 3:
            dx =  self.speed * 0
        elif randomMove == 4:
            dx =  self.speed * 1
        elif randomMove == 5:
            dx =  self.speed * 2
        elif randomMove == 6:
            dx =  self.speed * 3

        if self.rect.left + dx < 130:
            dx = 130 - self.rect.left
        if self.rect.right + dx > ((BACKGROUND_BAR[0] + BACKGROUND_BAR[2]) - (self.rect.width /2 )):
            dx =  ((BACKGROUND_BAR[0] + BACKGROUND_BAR[2]) - (self.rect.width /2 )) - self.rect.right

        self.rect.x += dx


    #def to move the sensors with the input from the sensor
    def sensor_move(self,surface,sensorData):
        dx = 0

        if sensorData > 30:
            dx = self.speed * 2

        if sensorData < 30 and sensorData > 24:
            dx = self.speed  * 3    
        elif sensorData < 24 and sensorData > 18 :
            dx =  self.speed * 2
        elif sensorData == 15:
            dx = self.speed * 0
        elif sensorData <18 and sensorData > 15:
            dx = self.speed * 1
        elif sensorData < 15 and sensorData > 12:
            dx = -self.speed * 1 
        elif sensorData < 12 and sensorData > 6:
            dx = -self.speed * 2
        elif sensorData < 6 and sensorData > 0:
            dx = -self.speed * 3
        

        if self.rect.left + dx < 130:
            dx = 130 - self.rect.left
        if self.rect.right + dx > ((BACKGROUND_BAR[0] + BACKGROUND_BAR[2]) - (self.rect.width /2 )):
            dx =  ((BACKGROUND_BAR[0] + BACKGROUND_BAR[2]) - (self.rect.width /2 )) - self.rect.right

        self.rect.x += dx
       
    #Drawing the bars
    def draw(self, surface, offset_height,color):
        bar_image = pygame.image.load("assets/images/background/bar_background_2.png").convert_alpha()
        background_bar_1 = pygame.Rect(BACKGROUND_BAR[0],BACKGROUND_BAR[1] + offset_height,BACKGROUND_BAR[2],BACKGROUND_BAR[3])
        surface.blit(bar_image,background_bar_1)

        bar_random_image = pygame.image.load("assets/images/background/random_bar.png").convert_alpha()
        attacking_bar = pygame.Rect(self.rect.centerx,self.rect.y -1, self.rect.width, self.rect.height)
        surface.blit(bar_random_image,attacking_bar)

    #Drawing the sensors
    def drawSensor(self,surface,color):
        bar_sensor_image = pygame.image.load("assets/images/background/sensor_bar.png").convert_alpha()
        attacking_bar_sensor = pygame.Rect(self.rect.centerx +10,self.rect.y + 1, self.rect.width -20, self.rect.height)
        surface.blit(bar_sensor_image,attacking_bar_sensor )

