import pygame as pg
import sys,time
from Bird import Bird
from pipe import Pipe

pg.init()      #Initialize all pygame modules 
pg.mixer.init()  # Initialize the mixer for sound

class Game:
    def __init__(self):        # Self refers to the specific object being created 
        # Setting Window Configuration
        self.width = 600
        self.height = 690
        self.scale_factor=1.5
        self.win=pg.display.set_mode((self.width,self.height)) #Create and store the game window 
        self.clock=pg.time.Clock() # we create clock object 
        self.move_speed=250
        self.start_monitoring=False
        self.hit_sound_played = False
        self.score=0
        self.last_speed_increase_score = 0
        self.font=pg.font.Font("assets/font.ttf",24)
        self.score_text=self.font.render("Score: 0",True,(255,255,255))
        self.score_text_rect=self.score_text.get_rect(center=(100,30))
        
        self.restart_text=self.font.render("Restart",True,(0,0,0))
        self.restart_text_rect=self.restart_text.get_rect(center=(300,600))
        self.gameover_text = self.font.render("GAME OVER", True, (255, 0, 0))
        self.gameover_text_rect = self.gameover_text.get_rect(center=(300, 300))

        # Load Sound Effects
        self.flap_sound = pg.mixer.Sound("assets/flap.wav")
        self.score_sound = pg.mixer.Sound("assets/score.wav")
        self.sound_hit=pg.mixer.Sound("assets/hit.wav")


        # Load high score from file
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except FileNotFoundError:
            self.high_score = 0  # If no file, start with 0

        self.bird=Bird(self.scale_factor)  # We pass scale factor to Bird object to scale it 
        self.is_enter_pressed=False
        self.is_game_started=True
        self.pipes=[]  # We create pipes list in which current no pipes are present, its empty at begining
        self.pipe_generate_counter=71
        self.setUpBgandGround()    
        self.gameLoop()
        

    def gameLoop(self):
        last_time=time.time()
        while True:   #we create infinite loop
            # Calculating delta time #
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time
            for event in pg.event.get():   #pygame store all the events, we run for loop on events to get any event which we required
                if event.type == pg.QUIT:
                    pg.quit()  #we call pg.quit() method to close pygame only
                    sys.exit()  #to close loop we use sys module and from this we call sys.exit() method 
                if event.type==pg.KEYDOWN and self.is_game_started:
                    if event.key==pg.K_RETURN:          #Return = enter Key
                        self.is_enter_pressed=True
                        self.bird.update_on=True
                    if event.key==pg.K_SPACE and self.is_enter_pressed: #We only press space key when enter pressed
                        self.bird.flap(dt)
                        self.flap_sound.play()
                if event.type==pg.MOUSEBUTTONDOWN:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()

                    
            self.updateEverything(dt) # Before drawing we have to update everything 
            self.checkcollsions()
            self.checkScore()
            self.drawEverything()
            pg.display.update() #If we dont update,so nothing shows on Window
            self.clock.tick(60)  # We lock game to run only at 60 fps

    def restartGame(self):
        self.score = 0
        self.score_text = self.font.render("Score: 0", True, (0,0,0))
        self.is_enter_pressed = False
        self.is_game_started = True
        self.bird.resetPosition()
        self.pipes.clear()
        self.pipe_generate_counter = 71
        self.bird.update_on = False
        # Reset collision sound flags
        self.hit_pipe_played = False
        self.hit_ground_played = False


    def checkScore(self):
        if len(self.pipes)>0:
            if (self.bird.rect.left>self.pipes[0].rect_down.left and
            self.bird.rect.right<self.pipes[0].rect_down.right and not self.start_monitoring):
                self.start_monitoring=True
            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring:
                self.start_monitoring=False
                self.score+=1
                self.score_text=self.font.render(f"Score: {self.score}",True,(255,255,255))
                self.score_sound.play()  # Play score sound

                if self.score % 5 == 0 and self.score != self.last_speed_increase_score:
                    self.move_speed *= 1.05
                    self.last_speed_increase_score = self.score


    def checkcollsions(self):
        if len(self.pipes):
            # Pipe collision
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
                self.bird.rect.colliderect(self.pipes[0].rect_up)):
                if not getattr(self, "hit_pipe_played", False):
                    self.sound_hit.play()
                    self.hit_pipe_played = True
                self.is_enter_pressed = False
                self.bird.update_on = True    # gravity still affects bird
                self.bird.flap_speed = 0

            # Ground collision
            if self.bird.rect.bottom >= 500:
                self.bird.rect.bottom = 500
                self.bird.y_velocity = 0
                self.bird.update_on = False
                self.is_enter_pressed = False
                self.is_game_started = False
                # Play ground sound only if bird did NOT hit pipe first
                if not getattr(self, "hit_pipe_played", False) and not getattr(self, "hit_ground_played", False):
                    self.sound_hit.play()
                    self.hit_ground_played = True

            # Update high score if game over
            if not self.is_game_started and self.score > self.high_score:
                self.high_score = self.score
                with open("highscore.txt", "w") as f:
                    f.write(str(self.high_score))

                
    def updateEverything(self,dt):
        if self.is_enter_pressed:     #if enter pressed then all the code below runs otherwise not
            # moving the ground
            self.ground1_rect.x-=int(self.move_speed*dt)
            self.ground2_rect.x-=int(self.move_speed*dt)

            if self.ground1_rect.right<0:
                self.ground1_rect.x=self.ground2_rect.right
            if self.ground2_rect.right<0:
                self.ground2_rect.x=self.ground1_rect.right
            
            # generating pipes
            if self.pipe_generate_counter>71:
                self.pipes.append(Pipe(self.scale_factor,self.move_speed))  #So we append 1 pipe in pipes list
                self.pipe_generate_counter=0 #we reset pipe generate counter to 0
            self.pipe_generate_counter+=1 # we increarse by 1

            #moving pipes
            for pipe in self.pipes:
                pipe.update(dt)

            #removing pipes if out of screen
            if len(self.pipes)!=0: # If pipe list is not empty
                if self.pipes[0].rect_up.right<0: #if right side corner of 0th index pipe becomes less than 0
                    self.pipes.pop(0) #so delete the 0th index pipe
            


         #moving the Bird
        self.bird.update(dt)   # Update bird position and animation 


    def drawEverything(self):

        self.win.blit(self.bg_img,(0,-320))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img,self.ground1_rect)
        self.win.blit(self.ground2_img,self.ground2_rect)
        self.win.blit(self.bird.image,self.bird.rect)
        self.win.blit(self.score_text,self.score_text_rect)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(450, 30))
        self.win.blit(high_score_text, high_score_rect)

        if not self.is_game_started:
            self.win.blit(self.restart_text,self.restart_text_rect)
        if not self.is_game_started:
            self.win.blit(self.gameover_text, self.gameover_text_rect)
        


    def setUpBgandGround(self):
        # Loading images for bg and ground
        self.bg_img=pg.transform.scale_by(pg.image.load("assets/bg.png").convert(),self.scale_factor) #pygame call load function from image module, pygame call scale_by function from transform module
        self.ground1_img=pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)
        self.ground2_img=pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)

        self.ground1_rect=self.ground1_img.get_rect() #We consider rectangle aroud ground1 img to get its parameters(x,y position,heigth etc)
        self.ground2_rect=self.ground2_img.get_rect() 

        #x-cordinates of ground
        self.ground1_rect.x=0
        self.ground2_rect.x=self.ground1_rect.right

        #y-coordinates of ground
        self.ground2_rect.y=500 # y cordinate remains same bcuz only ground move in x axis
        self.ground1_rect.y=500
game=Game()

                    
    
