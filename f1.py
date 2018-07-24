import pygame,math,sys,os
from pygame.locals import *
from random import randint

dir = '/home/pi/Desktop/frogger-master/Sprites/'

#class for the life sprite is the bottom right corner
class Lives(pygame.sprite.Sprite):
        def __init__(self,gs=None,pos=None):
                pygame.sprite.Sprite.__init__(self)

                self.gs = gs
                self.pos = pos

                self.image = pygame.image.load('Sprites/heart.png')
                self.image = pygame.transform.scale(self.image, (25,25))
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(self.pos,370)
    
#class for the floating objects in the river
class Floaters(pygame.sprite.Sprite):
        def __init__(self,gs=None, number=None,pos=None):
                pygame.sprite.Sprite.__init__(self)

                self.gs = gs
                self.number = number
                global dir

                #images of the objects
                self.objects = [dir+'boat1.png',dir+'boat1.png',dir+'boat1.png',dir+'boat1.png']
                self.pos = [460,520,420,560]
                self.speed = [1.8,1.6,1.9, 2.5]
                self.count = 1
                #loading image
                self.image = pygame.image.load(self.objects[number])
                self.image = pygame.transform.scale(self.image, (35,19))
                self.rect = self.image.get_rect()
                
                if self.number == 2:
                        self.rect = self.rect.move(self.pos[number],205)
                elif self.number == 1:
                        self.rect = self.rect.move(self.pos[number],10)
                elif self.number == 3:
                        self.rect = self.rect.move(self.pos[number],10)
                else:
                        self.rect = self.rect.move(self.pos[number],400)

        def tick(self,counter=None):
                if self.number % 2 == 0:
                        self.rect = self.rect.move(0,-1*self.speed[self.number])
                else:
                        self.rect = self.rect.move(0,self.speed[self.number])
        
#class for the cars
class Cars(pygame.sprite.Sprite):
        def __init__(self, gs=None, number=None):
                pygame.sprite.Sprite.__init__(self)

                self.gs = gs
                self.number = number
                global dir

                #cars image and location list
                self.cars = [dir+'car1.png',dir+'car2.png',dir+'car3.png', dir+'car1.png']
                self.pos = [195,280,370,130]
                self.speed = [1.9,2.1,1.8, 2.3]

                #loading image
                self.image = pygame.image.load(self.cars[number])
                self.image = pygame.transform.scale(self.image, (19,35))
                self.rect = self.image.get_rect()
                if self.number == 2:
                        self.rect = self.rect.move(self.pos[number],400)
                elif self.number == 1:
                        self.rect = self.rect.move(self.pos[number],10)
                elif self.number == 3:
                        self.rect = self.rect.move(self.pos[number],10)
                else:
                        self.rect = self.rect.move(self.pos[number],400)

        def tick(self):
                if self.number % 2 == 0:
                        self.rect = self.rect.move(0,-1*self.speed[self.number])
                else:
                        self.rect = self.rect.move(0,self.speed[self.number])

                
class Player(pygame.sprite.Sprite):
        def __init__(self,gs=None):
                pygame.sprite.Sprite.__init__(self)

                self.gs = gs
                self.image = pygame.image.load("Sprites/myrtle1.e.png")
                self.image = pygame.transform.scale(self.image, (37,67))
                
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(5,225)

                #sprite movement counts
                self.up_count = 1
                self.down_count = 1
                self.right_count = 1
                self.left_count = 1
                self.timer = 0

        def tick(self):
                if self.gs.pressed["right"] == True:
                        self.rect = self.rect.move(5,0)
                if self.gs.pressed["left"] == True:
                        self.rect = self.rect.move(-5,0)
                if self.gs.pressed["up"] == True:
                        self.rect = self.rect.move(0,-5)
                if self.gs.pressed["down"] == True:
                        self.rect = self.rect.move(0,5)

                #increment counter
                self.timer = self.timer + 1
        
                        
class GameSpace:
        def player_hit(self,car):
                if self.player.rect.colliderect(car.rect):
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect = self.player.rect.move(5,225)
                        self.lives = self.lives - 1
                        self.lives_list.pop()
                                                
        def player_float(self,obj):
                if self.player.rect.colliderect(obj.rect):
                        self.player.rect = self.player.rect.move(0,obj.speed[obj.number])
                
        def inbounds(self,car,lst):
                if car.rect[1] >= 0 and car.rect[1] <= 410:
                        lst.append(car) 
        
        def outofbounds(self):
            if self.player.rect[1] < -5 or self.player.rect[1] > 400:
                    self.player.rect = self.player.image.get_rect()
                    self.player.rect = self.player.rect.move(5,225)
            if self.player.rect[0] < -5:
                    self.player.rect = self.player.image.get_rect()
                    self.player.rect = self.player.rect.move(5,225)
                        
        def game_screen(self):
                pygame.init()

                #screen size and background
                self.size = self.width, self.height = 760,410
                self.bg = pygame.image.load("Sprites/backg1.JPG")
                self.go = pygame.image.load("Sprites/gameover.png")
                self.bg = pygame.transform.scale(self.bg, (760,410))
                self.black = 0,0,0

                #initialize text
                self.font = pygame.font.SysFont("monospace",25)

                #variables for object generation
                self.object_list = []
                self.temp_object = []

                #variables for car generation
                self.counter = 0
                self.car_list = []
                self.temp_car = []
                
                
        def frog_start(self):
                #creating lives image
                self.lives_list = []
                self.lives_list.append(Lives(self,730))
                self.lives_list.append(Lives(self,700))
                self.lives_list.append(Lives(self,670))

                #creating game objects
                self.player = Player(self)
                self.score1 = 0

                #setting up screen
                self.screen = pygame.display.set_mode(self.size)
                self.clock = pygame.time.Clock()

                #gameplay variables
                self.lives = 3

        def wait(self):
                while True:
                        event = pygame.event.wait()
                        if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                        if event.type == KEYDOWN and event.key == K_y:
                                break
                        if event.type == KEYDOWN and event.key == K_n:
                                pygame.quit()
                                sys.exit()
                                
                                
        def frog_restart(self):
                self.lives = 3

                #creating lives image
                self.lives_list = []
                self.lives_list.append(Lives(self,730))
                self.lives_list.append(Lives(self,700))
                self.lives_list.append(Lives(self,670))

                self.pressed = {"up":False, "down":False, "right":False, "left":False,"w":False, "s":False, "d":False, "a":False}

                self.player.rect = self.player.image.get_rect()
                self.player.rect = self.player.rect.move(5,225)

                self.screen.fill(self.black)
                self.screen.blit(self.go,(0,0))

                pygame.display.flip()

                self.wait()
                

        def main(self):

                self.game_screen()

                self.frog_start()

                #pressed keys
                self.pressed = {"up":False, "down":False, "right":False, "left":False,"w":False, "s":False, "d":False, "a":False}

                #starting game loop
                while 1:
                        #handle user inputs
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        sys.exit()

                                if event.type == KEYDOWN:
                                        if(event.key == pygame.K_RIGHT):
                                                self.pressed['right'] = True
                                        if(event.key == pygame.K_LEFT):
                                                self.pressed['left'] = True
                                        if(event.key == pygame.K_UP):
                                                self.pressed['up'] = True
                                        if(event.key == pygame.K_DOWN):
                                                self.pressed['down'] = True

                                if event.type == KEYUP:
                                        if(event.key == pygame.K_RIGHT):
                                                self.pressed['right'] = False
                                        if(event.key == pygame.K_LEFT):
                                                self.pressed['left'] = False
                                        if(event.key == pygame.K_UP):
                                                self.pressed['up'] = False
                                        if(event.key == pygame.K_DOWN):
                                                self.pressed['down'] = False
                          
                        #generating Cars
                        if self.counter % 50 == 0:
                                if randint(0,2) == 0:
                                        self.car_list.append(Cars(self,0))
                        if self.counter % 50 == 0:
                                if randint(0,4) == 1:
                                        self.car_list.append(Cars(self,1))
                        if self.counter % 50 == 0:
                                if randint(0,3) == 0:
                                        self.car_list.append(Cars(self,2))
                        if self.counter % 50 == 0:
                                if randint(0,4) == 0:
                                        self.car_list.append(Cars(self,3))

                        #generating objects:
                        if self.counter % 200 == 0:
                                self.object_list.append(Floaters(self,0))
                        if self.counter % 210 == 0:
                                self.object_list.append(Floaters(self,1))
                        if self.counter % 220 == 0:
                                self.object_list.append(Floaters(self,2))
                        if self.counter % 220 == 0:
                                self.object_list.append(Floaters(self,3))
                                
                        #Clock and Object ticks
                        self.clock.tick(60)
                        self.player.tick()
                        
                        for car in self.car_list:
                                car.tick()
                                self.inbounds(car,self.temp_car)
                                self.player_hit(car)

                        if self.lives == 0:
                                self.frog_restart()
                                continue

                        for obj in self.object_list:
                                obj.tick(self.counter)
                                self.inbounds(obj,self.temp_object)
                                if self.player.rect[0] >=375:
                                        self.player_float(obj)
                                        
                        if self.player.rect[0] > 700:
                                self.score1 += 1
                                self.player.rect = self.player.image.get_rect()
                                self.player.rect = self.player.rect.move(5,225)
                                
                        #Checks if frogger is out of bounds
                        self.outofbounds()

                        #Checks if lives are gone

                        #clearing the off screen cars
                        self.car_list = self.temp_car
                        self.temp_car = []

                        #clearing off screen floaters
                        self.object_list = self.temp_object
                        self.temp_object = []

                        self.counter = self.counter + 1
                        #send tick to game objects

                        #display
                        self.screen.fill(self.black)
                        self.screen.blit(self.bg,(0,0))

                        for car in self.car_list:
                                self.screen.blit(car.image,car.rect)

                        for obj in self.object_list:
                                self.screen.blit(obj.image,obj.rect)
                                

                        for life in self.lives_list:
                                self.screen.blit(life.image,life.rect)
                        self.screen.blit(self.player.image, self.player.rect)
                        

                        #displaying text
                        score1 = self.font.render("SCORE: " + str(self.score1),1,(255,255,0))
                        self.screen.blit(score1,(0, 15))

                        pygame.display.flip()


if __name__ == '__main__':
        gs = GameSpace()
        gs.main() 
