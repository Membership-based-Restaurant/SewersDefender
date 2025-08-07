import pygame
import sys
import loadresources
import time
import enemies
import towers
import ammunition
import maps
import entities
from constants import *
import settings


class Game:
    def __init__(self):
        # preparation
        pygame.init()
        self.set = settings.Settings()
        self.screen = pygame.display.set_mode(self.set.screenSize)
        self.res = loadresources.ImgRes()
        pygame.display.set_caption('Test')
        pygame.display.set_icon(self.res.icon)
        self.ifPlayGame = True
        # game res
        self.map = maps.Map(self)
        self.map.map_blit()
        pygame.display.flip()
        self.enemyManager = enemies.EnManager(self)
        self.towerManager = towers.ToManager(self)
        self.ammoManager = ammunition.AmManage(self)
        self.messageManager = entities.MeManager(self)
        self.ifOperating = False
        self.selectedTower = None
        self.ifPause = False
        self.ifExecuteTasks = True

    def run_game(self):
        while self.ifPlayGame:
            startTime = time.time()
            self.check_event()
            if self.ifExecuteTasks:
                self.execute_task()
            self.update_entities()
            self.update_screen()
            flag = self.judge_game()
            if flag == WIN:
                print('Win')
            elif flag == LOSE:
                print('Lose')
            else:
                pass
            endTime = time.time()
            runTime = endTime-startTime
            if runTime < 1/60:
                time.sleep(1/60-runTime)
        pygame.quit()
        sys.exit()

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # operate
                if self.towerManager.ifOperating:
                    print('Operatingmode:', event.button)

                    if event.button == 1:
                        if self.towerManager.operateButtonManager.check_bu_list(event.pos):
                            self.towerManager.operateButtonManager.clear_bu_list()
                            self.towerManager.create_operateButtons()
                        else:
                            self.towerManager.quit_operatingmode()
                    else:
                        self.towerManager.quit_operatingmode()

                # select tower
                if not self.towerManager.ifOperating:
                    if event.button == 1:
                        self.towerManager.select_tower(event.pos)
                        if self.towerManager.ifOperating:
                            self.towerManager.create_operateButtons()
                else:
                    pass
        pygame.event.pump()

    def excute_event(self):
        pass

    def execute_task(self):
        taskDict = self.map.get_task_dict(UPDATE)
        if END in taskDict.values():
            self.ifExecuteTasks = False
        else:
            for routeNum in range(self.map.numRoutes):
                if routeNum in taskDict.keys():
                    task = taskDict[routeNum]
                    if task == REST:
                        pass
                    else:
                        self.enemyManager.create_enemy(task, routeNum)

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
        self.towerManager.operateButtonManager.blit_bu_list()
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run_game()
