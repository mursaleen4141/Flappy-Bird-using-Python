import pygame as pg
class Bird(pg.sprite.Sprite):   #We inherit Sprite class from sprite module so that our bird adopt all sprite features#
    def __init__ (self,scale_factor):
        super(Bird,self).__init__() #we create super class and initialize it
        self.img_list=[pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(),scale_factor),
                       pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(),scale_factor)]
        self.image_index=0
        self.image=self.img_list[self.image_index] # we initially set 0th index image 
        self.rect=self.image.get_rect(center=(100,100))  # we consider rectangle around 0th ndex image and pass tuple( position of placing bird)
        self.y_velocity=0
        self.gravity=10
        self.flap_speed=250
        self.anim_counter=0
        self.update_on=False

    def update(self,dt):
        if self.update_on:
            self.playAnimation()        #before apply gravity we have to update animation
            self.applyGravity(dt)

            if self.rect.y<=0: #if we want to move above from y=0
                self.rect.y=0  # we stuck at y=0
                self.flap_speed=0 #And consider flap speed=0 so bird stuck at y=0
            elif self.rect.y>=0 and self.flap_speed==0:  
                self.flap_speed=250                      
        
    def applyGravity(self,dt):
        self.y_velocity+=self.gravity*dt #y coordinate velocity increases with gravity
        self.rect.y+=self.y_velocity     #the y position of bird increases with velocity along y axis
    
    def flap(self,dt):
        self.y_velocity=-self.flap_speed*dt

    def playAnimation(self):
        if self.anim_counter==5:    
            self.image=self.img_list[self.image_index]
            if self.image_index==0: self.image_index=1 
            else: self.image_index=0
            self.anim_counter=0 # we reset anim counter to 0

        self.anim_counter+=1

    def resetPosition(self):
        self.rect.center=(100,100)
        self.y_velocity=0
        self.anim_counter=0
        

                



