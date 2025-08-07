import pygame,sys
import loadresources
import time
import enemies,towers
import ammunition
import maps
import entities
from constants import *
import settings
class Game:
    def __init__(self):
        #preparation
        pygame.init()
        self.set=settings.Settings()
        self.screen=pygame.display.set_mode(self.set.screenSize)
        self.res=loadresources.ImgRes()
        pygame.display.set_caption('Test')
        pygame.display.set_icon(self.res.icon)
        self.ifPlayGame=True
        #game res
        self.map=maps.Map(self)
        self.map.map_blit()
        pygame.display.flip()
        self.enemyManager=enemies.EnManager(self)
        self.towerManager=towers.ToManager(self)
        self.ammoManager=ammunition.AmManage(self)
        self.messageManager=entities.MeManager(self)
        #execute tasks
        self.ifPause=False
        self.ifExecuteTasks=True
        self.taskType=maps.taskType
     
    def run_game(self):
        while self.ifPlayGame:
            startTime=time.time()
            self.check_event()
            if self.ifExecuteTasks:
                self.execute_task()            
            self.update_entities()
            self.update_screen()
            '''flag=self.judge_game()
            if flag == WIN:
                print('Win')
            elif flag == LOSE:
                print('Lose')
            else:
                pass'''
            endTime=time.time()
            runTime=endTime-startTime
            time.sleep(1/60-runTime)
        pygame.quit()
        sys.exit()
            
    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #operate
                if self.towerManager.ifOperating:
                    print('Operatingmode:',event.button)
                    tower=self.towerManager.selectedTower
                    if event.button == 1:
                        if tower.ifUpgradeable and tower.upgradebox.collidepoint(event.pos):
                            num=int((event.pos[1]-tower.upgradebox.top)/UP_WIDTH)
                            self.towerManager.upgrade_tower(tower,num)
                        else:
                            tower.ifSelected=False
                            self.towerManager.ifOperating=False#if upgrade, remain operating mode
                        print('Exit operatingmode')
                        pass
                        
                    elif event.button == 3:
                        if tower.hitbox.collidepoint(event.pos):
                            self.towerManager.delete_tower(tower)
                        else:
                            tower.ifSelected=False
                        self.towerManager.ifOperating=False
                        print('Exit operatingmode')
                        pass
                #select tower    
                if not self.towerManager.ifOperating:
                    if event.button == 1:
                        tower=self.towerManager.search_tower(event.pos)
                        if tower == False:
                            pass
                        else:
                            print('Operating')
                            self.towerManager.ifOperating=True
                            self.towerManager.selectedTower=tower
                            tower.ifSelected=True 
                else:
                    pass
        pygame.event.pump()
                        
    def excute_event(self):
        pass     
                    
    def execute_task(self):
        taskDict=self.map.get_task_dict(UPDATE)
        if END in taskDict.values():
            self.ifExecuteTasks=False
        else:
            for routeNum in range(self.map.numRoutes):
                if routeNum in taskDict.keys():
                    task=taskDict[routeNum]
                    if task == REST:
                        pass
                    else:
                        self.enemyManager.create_enemy(task,routeNum)
                        
    def judge_game(self):
        if self.map.finishManager.if_lose():
            return LOSE
        if self.enemyManager.enemyKilledNum == self.map.numEnemies:
            return WIN
        return UNDECIDED
                            
    def update_entities(self):
        self.enemyManager.manage_en_list()
        self.towerManager.manage_to_list()
        self.ammoManager.manage_am_list()
        self.messageManager.manage_me_list()
    
    def update_screen(self):
        self.map.map_blit()
        self.map.finishManager.blit_fin_list()
        self.towerManager.blit_to_list()
        self.enemyManager.blit_en_list()
        self.ammoManager.blit_am_list()
        self.messageManager.blit_me_list()
        pygame.display.flip()
     
if __name__ == '__main__':        
    game=Game()
    game.run_game()