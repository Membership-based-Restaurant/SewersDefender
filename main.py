import pygame
import sys
import os.path as op
import loadresources
import time
import enemies
import towers
import ammunition
import maps
import entities
import constants as c
import settings
from typing import override


class PaManager:
    def __init__(self):
        pygame.init()
        self.ifRunPage = True
        self.set = settings.Settings(self)
        self.volume = self.set.defaultVolume
        self.musicPath = self.set.defaultMusicPath
        self.screen = pygame.display.set_mode(self.set.screenSize)
        self.res = loadresources.ImgRes()
        pygame.display.set_icon(self.res.icon)
        self.set_pages()
        self.currentPage = self.welcome
        # music
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.load(self.musicPath)
        pygame.mixer.music.play(-1)

    def set_pages(self):
        self.welcome = Welcome(self.screen, self.res, self)
        self.select = Select(self.screen, self.res, self)
        self.pause = Pause(self.screen, self.res, self)
        self.concludeWin = ConcludeWin(self.screen, self.res, self)
        self.concludeLose = ConcludeLose(self.screen, self.res, self)
        self.game = Game(self.screen, self.res, self)
        self.settings = Settings(self.screen, self.res, self)
        self.welcome.pa_set()
        self.select.pa_set()
        self.pause.pa_set()
        self.concludeWin.pa_set()
        self.concludeLose.pa_set()
        self.game.pa_set()
        self.settings.pa_set()

    def manage_pages(self):
        while self.ifRunPage:
            startTime = time.time()
            self.currentPage.pa_run()
            pygame.display.flip()
            endTime = time.time()
            runTime = endTime - startTime
            if runTime < 1 / 60:
                time.sleep(1 / 60 - runTime)

    def quit_program(self):
        self.set.save_music_set()


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
        pygame.display.set_caption("Test")
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
    @override
    def pa_set(self):
        self.img = pygame.image.load("resources/bkwe.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.EnterButton(self.pageManager.select, (600, 400))
        )
        self.buttonManager.buttonList.append(
            entities.SettingsButton(self.pageManager.settings, (600, 500))
        )
        self.buttonManager.buttonList.append(entities.ExitButton(self, (600, 600)))
        pass


class Settings(Page):
    @override
    def pa_set(self):
        self.img = pygame.image.load("resources/bkse.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.welcome, (57, 40))
        )
        self.buttonManager.buttonList.append(
            entities.MusicChooseButton(self, "bgm/bgm1 by tttiw.ogg", (600, 150))
        )
        self.buttonManager.buttonList.append(
            entities.MusicChooseButton(self, "bgm/bgm2 by tttiw.ogg", (600, 250))
        )
        self.buttonManager.buttonList.append(
            entities.MusicChooseButton(self, "bgm/bgm3 by tttiw.ogg", (600, 350))
        )
        self.buttonManager.buttonList.append(entities.VolumeUpButton(self, (910, 760)))
        self.buttonManager.buttonList.append(
            entities.VolumeDownButton(self, (1103, 760))
        )
        pass

    @override
    def pa_blit(self):
        self.screen.blit(self.img, self.screen_rect)
        self.blit_info()
        self.buttonManager.blit_bu_list()

    def blit_info(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        temptImg1 = font.render(
            f"CurrentVolume:{round(self.pageManager.volume, 1)}",
            True,
            (239, 228, 176),
        )
        temptImg2 = font.render(
            f"CurrentMusic:{op.splitext(op.basename(self.pageManager.musicPath))[0]}",
            True,
            (239, 228, 176),
        )
        infoImg = pygame.Surface((1200, temptImg1.get_height() * 2 + 10))
        infoImg.fill((135, 75, 24))
        pygame.draw.rect(infoImg, (239, 228, 176), infoImg.get_rect(), 1)
        infoImg.blit(temptImg1, (10, 5 + temptImg1.get_height()))
        infoImg.blit(temptImg2, (10, 5))
        self.screen.blit(infoImg, (0, 658))


class Select(Page):
    @override
    def pa_set(self):
        self.img = pygame.image.load("resources/bks.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.MapChooseButton(
                "game_maps/map1/", self.pageManager.game, (600, 200)
            )
        )
        self.buttonManager.buttonList.append(
            entities.MapChooseButton(
                "game_maps/map2/", self.pageManager.game, (600, 400)
            )
        )
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.welcome, (57, 40))
        )
        pass


class ConcludeWin(Page):
    @override
    def pa_set(self):
        self.img = pygame.image.load("resources/bkw.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.GameRestartButton(self.pageManager.game, (600, 400))
        )
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.select, (600, 760))
        )
        self.buttonManager.buttonList.append(entities.ExitButton(self, (600, 760)))
        pass


class ConcludeLose(Page):
    @override
    def pa_set(self):
        self.img = pygame.image.load("resources/bkl.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.GameRestartButton(self.pageManager.game, (600, 400))
        )
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.select, (600, 500))
        )
        self.buttonManager.buttonList.append(entities.ExitButton(self, (600, 600)))
        pass


class Pause(Page):
    @override
    def pa_set(self):
        self.img = pygame.image.load("resources/bkp.png").convert_alpha()
        self.buttonManager.buttonList.append(
            entities.GameRestartButton(self.pageManager.game, (600, 400))
        )
        self.buttonManager.buttonList.append(
            entities.BackButton(self.pageManager.select, (600, 500))
        )
        self.buttonManager.buttonList.append(
            entities.GameContinueButton(self.pageManager.game, (600, 600))
        )
        self.buttonManager.buttonList.append(entities.ExitButton(self, (600, 700)))
        pass


class Game(Page):
    @override
    def pa_set(self):
        self.set_buttons()
        self.mapPath = ""

    def set_buttons(self):
        self.buttonManager.clear_bu_list()
        self.buttonManager.buttonList.append(
            entities.GamePauseButton(self.pageManager.pause, (1135, 38))
        )
        self.buttonManager.buttonList.append(entities.TaskStartButton(self, (55, 113)))

    def set_game_resources(self):
        self.map = maps.Map(self, self.mapPath)
        self.enemyManager = enemies.EnManager(self)
        self.buffManager = enemies.BuffManager(self)
        self.towerManager = towers.ToManager(self)
        self.ammoManager = ammunition.AmManage(self)
        self.messageManager = entities.MeManager(self)
        self.ifPlayGame = True
        self.ifExecuteTasks = False
        self.ifTaskEnd = False

    @override
    def pa_run(self):
        pygame.display.set_caption("Gaming")
        self.check_event()
        if self.ifExecuteTasks:
            self.execute_task()
        self.update_entities()
        self.update_screen()
        flag = self.judge_game()
        if flag == c.GameJudge.WIN:
            self.pageManager.currentPage = self.pageManager.concludeWin
        elif flag == c.GameJudge.LOSE:
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
                    print("Operatingmode:", event.button)
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
        taskDict = self.map.get_task_dict(c.MapTaskType.UPDATE)
        if not taskDict:
            return
        if taskDict.get(0) == c.TaskEvent.END and len(taskDict) == 1:
            self.ifExecuteTasks = False
            self.ifTaskEnd = True
            return
        for routeNum, task in taskDict.items():
            if isinstance(task, c.TaskEvent):
                continue
            self.enemyManager.create_enemy(task, routeNum)

    def judge_game(self):
        if self.map.finishManager.if_lose():
            return c.GameJudge.LOSE
        if self.ifTaskEnd and len(self.enemyManager.enemyList) == 0:
            return c.GameJudge.WIN
        return c.GameJudge.UNDECIDED

    def update_entities(self):
        self.enemyManager.manage_en_list()
        self.buffManager.manage_buff_list()
        self.towerManager.manage_to_list()
        self.ammoManager.manage_am_list()
        self.messageManager.manage_me_list()

    def blit_info(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        temptImg1 = font.render(
            f"Money:{self.map.money:d}".format(), True, (239, 228, 176)
        )
        temptImg2 = font.render(
            f"Wave:{self.map.currentWave + 1:d}".format(), True, (239, 228, 176)
        )
        temptImg3 = font.render(
            f"EnemyKilled:{self.enemyManager.enemyKilledNum:d}".format(),
            True,
            (239, 228, 176),
        )
        infoImg = pygame.Surface((1200, temptImg1.get_height() + 10))
        infoImg.fill((135, 75, 24))
        pygame.draw.rect(infoImg, (239, 228, 176), infoImg.get_rect(), 1)
        infoImg.blit(temptImg1, (10, 5))
        infoImg.blit(temptImg2, (310, 5))
        infoImg.blit(temptImg3, (510, 5))
        self.screen.blit(infoImg, (0, 0))

    def update_screen(self):
        self.map.map_blit()
        self.map.finishManager.blit_fin_list()
        self.towerManager.blit_to_list()
        self.enemyManager.blit_en_list()
        self.buffManager.blit_buff_list()
        self.ammoManager.blit_am_list()
        self.blit_info()
        self.towerManager.operateButtonManager.blit_bu_list()
        self.buttonManager.blit_bu_list()
        self.messageManager.blit_me_list()


if __name__ == "__main__":
    p = PaManager()
    p.manage_pages()
