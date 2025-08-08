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


class PaManager:
    def __init__(self):
        pygame.init()
        self.ifRunPage = True
        self.set = settings.Settings()
        self.screen = pygame.display.set_mode(self.set.screenSize)
        self.res = loadresources.ImgRes()
        pygame.display.set_icon(self.res.icon)
        self.set_pages()
        self.currentPage = self.welcome
        pass

    def set_pages(self):
        self.welcome = Welcome(self.screen, self.res, self)
        self.select = Select(self.screen, self.res, self)
        self.pause = Pause(self.screen, self.res, self)
        self.concludeWin = ConcludeWin(self.screen, self.res, self)
        self.concludeLose = ConcludeLose(self.screen, self.res, self)
        self.game = Game(self.screen, self.res, self)
        self.welcome.pa_set()
        self.select.pa_set()
        self.pause.pa_set()
        self.concludeWin.pa_set()
        self.concludeLose.pa_set()
        self.game.pa_set()

    def manage_pages(self):
        while self.ifRunPage:
            startTime = time.time()
            self.currentPage.pa_run()
            pygame.display.flip()
            endTime = time.time()
            runTime = endTime-startTime
            if runTime < 1/60:
                time.sleep(1/60-runTime)
        pygame.quit()
        sys.exit()


class Page:
    def __init__(self, screen: pygame.Surface, res: loadresources.ImgRes, pageManager):
        # preparation
        self.pageManager = pageManager
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.res = res
        self.buttonManager = entities.BuManager(self)
        self.ifWorking = True

    def pa_set(self):
        self.img = pygame.image.load("").convert_alpha()  # example
        self.buttonManager.buttonList.append(None)  # example

    def pa_run(self):
        pygame.display.set_caption('Test')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.buttonManager.check_bu_list(event.pos)
        pygame.event.pump()
        self.pa_blit()

    def pa_blit(self):
        self.screen.blit(self.img, self.screen_rect)
        self.buttonManager.blit_bu_list()


class Welcome(Page):
    def pa_set(self):
        self.img = pygame.image.load("resources/bk.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.EnterButton(self.pageManager.select, (600, 400)))
        pass


class Select(Page):
    def pa_set(self):
        self.img = pygame.image.load("resources/bk.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.MapChooseButton('game_maps/map1/', self.pageManager.game, (600, 400)))
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.welcome, (60, 30)))
        pass


class ConcludeWin(Page):
    def pa_set(self):
        self.img = pygame.image.load("resources/bkw.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.GameRestartButton(self.pageManager.game, (600, 400)))
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.select, (600, 500)))
        pass


class ConcludeLose(Page):
    def pa_set(self):
        self.img = pygame.image.load("resources/bkl.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.GameRestartButton(self.pageManager.game, (600, 400)))
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.select, (600, 500)))
        pass


class Pause(Page):
    def pa_set(self):
        self.img = pygame.image.load("resources/bkp.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.GameRestartButton(self.pageManager.game, (600, 400)))
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.select, (600, 500)))
        self.buttonManager.buttonList.append(
            entities.GameContinueButton(self.pageManager.game, (600, 600)))
        pass


class Game(Page):
    def pa_set(self):
        self.set_buttons()
        self.mapPath = ""

    def set_buttons(self):
        self.buttonManager.clear_bu_list()
        self.buttonManager.buttonList.append(
            entities.GamePauseButton(self.pageManager.pause, (1135, 30)))
        self.buttonManager.buttonList.append(
            entities.TaskStartButton(self, (60, 30)))

    def set_game_resources(self):
        self.map = maps.Map(self, self.mapPath)
        self.enemyManager = enemies.EnManager(self)
        self.towerManager = towers.ToManager(self)
        self.ammoManager = ammunition.AmManage(self)
        self.messageManager = entities.MeManager(self)
        self.ifPlayGame = True
        self.ifExecuteTasks = False
        self.ifTaskEnd = False

    def pa_run(self):
        pygame.display.set_caption('Gaming')
        self.check_event()
        if self.ifExecuteTasks:
            self.execute_task()
        self.update_entities()
        self.update_screen()
        flag = self.judge_game()
        if flag == WIN:
            self.pageManager.currentPage = self.pageManager.concludeWin
        elif flag == LOSE:
            self.pageManager.currentPage = self.pageManager.concludeLose
        else:
            pass

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # operate
                if self.towerManager.ifOperating:
                    print('Operatingmode:', event.button)
                    if self.towerManager.operateButtonManager.check_bu_list(event.pos):
                        self.towerManager.operateButtonManager.clear_bu_list()
                        self.towerManager.create_operateButtons()
                    else:
                        self.towerManager.quit_operatingmode()
                # select tower
                if not self.towerManager.ifOperating:
                    self.towerManager.select_tower(event.pos)
                    if self.towerManager.ifOperating:
                        self.towerManager.create_operateButtons()
                self.buttonManager.check_bu_list(event.pos)
        pygame.event.pump()

    def execute_task(self):
        taskDict = self.map.get_task_dict(UPDATE)
        if END in taskDict.values():
            self.ifExecuteTasks = False
            self.ifTaskEnd = True
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
        if self.ifTaskEnd and len(self.enemyManager.enemyList) == 0:
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
        self.buttonManager.blit_bu_list()


if __name__ == '__main__':
    p = PaManager()
    p.manage_pages()
