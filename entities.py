import pygame
from constants import *

class Entity:
    def __init__(self,pos:tuple,game):
        
        self.screen=game.screen
        self.screen_rect=self.screen.get_rect()
        #basic data
        self.ifLiving=True
        self.pos=pos 
        #route
        self.set(game)
        self.img_rect=self.img.get_rect()
        self.img_rect.center=self.pos
        self.hitbox.center=self.pos
        
    def set(self,game):#example
        #img
        self.img=game.res.get_img(ET_FINISH)#example
        self.hitbox=self.img.get_rect().inflate(-5,-5)#example
        
    def et_blit(self):
        self.screen.blit(self.img,self.img_rect)
        pygame.draw.rect(self.screen,(0,255,0),self.hitbox,1)    
        
        
class Finish(Entity):
    def set(self,game):#example
        self.img=game.res.get_img(ET_FINISH)#example
        self.hitbox=self.img.get_rect().inflate(-5,-5)#example

class FinManager():
    def __init__(self,game):
        self.game=game
        self.finishList=[]
    
    def create_finish(self,pos:int):
        self.finishList.append(Finish(pos,self.game))
        
    def if_lose(self):
        for finish in self.finishList:
            for enemy in self.game.enemyManager.enemyList:
                if finish.hitbox.collidepoint(enemy.pos):
                    return True
                
    def blit_fin_list(self):
        for finish in self.finishList:
            finish.et_blit()


class Message():
    def __init__(self,screen:pygame.Surface,info:str,pos:tuple,size:int):
        self.screen=screen
        font=pygame.font.Font('resources/FanwoodText-Regular.ttf',size)
        self.img=font.render(info,True,(255,0,0))
        self.img_rect=self.img.get_rect()
        self.img_rect.center=pos
        self.me_set()
        
    def me_set(self):
        self.remainingTime=ME_R_TIME_D
    
    def me_blit(self):
        self.screen.blit(self.img,self.img_rect)
        self.remainingTime-=1

class MeManager():
    def __init__(self,game):
        self.game=game
        self.messageList=[]
        
    def create_message(self,info:str,pos:tuple,size:int):
        self.messageList.append(Message(self.game.screen,info,pos,size))
        
    def manage_me_list(self):
        temptList=[]
        for message in self.messageList:
            if message.remainingTime > 0:
                temptList.append(message)
            else:
                pass
        self.messageList=temptList
    
    def blit_me_list(self):
        for message in self.messageList:
            message.me_blit()
            
    def clear_me_list(self):
        self.messageList.clear()