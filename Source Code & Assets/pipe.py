import pygame as pg
from random import randint

class Pipe:     
    def __init__(self,scale_factor,move_speed):
        self.img_up=pg.transform.scale_by(pg.image.load("assets/pipeup.png").convert_alpha(),scale_factor)
        self.img_down=pg.transform.scale_by(pg.image.load("assets/pipedown.png").convert_alpha(),scale_factor)
        self.rect_up=self.img_up.get_rect()  #We consider rect around pipes
        self.rect_down=self.img_down.get_rect()
        self.pipe_distance=150
        self.rect_up.y=randint(250,520) ## Set a random vertical position for the upper pipe between 250 and 520 means the pipes generating was actually between those values

        self.rect_up.x=600        # The x position of pipe is same as window width so that pip starts from the right edge of the screen
        self.rect_down.y=self.rect_up.y-self.pipe_distance-self.rect_up.height  # To place pipedown image we use this formula
        self.rect_down.x=600 
        self.move_speed=move_speed
    
    def drawPipe(self,win):
        win.blit(self.img_up,self.rect_up)
        win.blit(self.img_down,self.rect_down)

    def update(self,dt):
        self.rect_up.x-=int(self.move_speed*dt)    # The x position of both pipes decreases with some speed
        self.rect_down.x-=int(self.move_speed*dt)
 