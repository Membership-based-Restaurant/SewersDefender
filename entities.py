import pygame
import towers
from constants import *


class Entity:
    def __init__(self, game, pos: tuple):
        self.game = game
        self.screen = self.game.screen
        self.ifLiving = True
        self.pos = pos
        self.et_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos

    def et_set(self):
        self.img = self.game.res.get_img(ET_FINISH)  # example
        self.hitbox = self.img.get_rect().inflate(-5, -5)  # example

    def et_blit(self):
        self.screen.blit(self.img, self.img_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), self.hitbox, 1)


class Finish(Entity):
    def et_set(self):  # example
        self.img = self.game.res.get_img(ET_FINISH)  # example
        self.hitbox = self.img.get_rect().inflate(-10, -10)  # example


class FinManager():
    def __init__(self, game):
        self.game = game
        self.finishList = []

    def create_finish(self, pos: int):
        self.finishList.append(Finish(self.game, pos))

    def if_lose(self):
        for finish in self.finishList:
            for enemy in self.game.enemyManager.enemyList:
                if finish.hitbox.collidepoint(enemy.pos):
                    return True

    def blit_fin_list(self):
        for finish in self.finishList:
            finish.et_blit()


class Message():
    def __init__(self, screen: pygame.Surface, info: str, pos: tuple, size: int):
        self.screen = screen
        font = pygame.font.Font('resources/FanwoodText-Regular.ttf', size)
        self.img = font.render(info, True, (255, 0, 0))
        self.img_rect = self.img.get_rect()
        self.img_rect.center = pos
        self.me_set()

    def me_set(self):
        self.remainingTime = ME_R_TIME_D

    def me_blit(self):
        self.screen.blit(self.img, self.img_rect)
        self.remainingTime -= 1


class MeManager():
    def __init__(self, game):
        self.game = game
        self.messageList = []

    def create_message(self, info: str, pos: tuple, size: int):
        self.messageList.append(Message(self.game.screen, info, pos, size))

    def manage_me_list(self):
        temptList = []
        for message in self.messageList:
            if message.remainingTime > 0:
                temptList.append(message)
            else:
                pass
        self.messageList = temptList

    def blit_me_list(self):
        for message in self.messageList:
            message.me_blit()

    def clear_me_list(self):
        self.messageList.clear()


class Button(Entity):
    def bu_check(self, pos: tuple):
        if self.hitbox.collidepoint(pos):
            return True
        else:
            return False

    def bu_work(self):
        pass


class TowerDeleteButton(Button):
    def __init__(self, game, tower):
        self.game = game
        self.pos = (tower.hitbox.centerx,
                    tower.hitbox.bottom+int(UP_WIDTH/2))
        self.screen = game.screen
        self.ifLiving = True
        self.et_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos
        self.tower = tower
        self.type = tower.towerType

    def et_set(self):
        temptImg = self.game.res.get_img(BU_TO_DELETE)
        self.img = pygame.transform.scale(temptImg, (UP_WIDTH, UP_WIDTH))
        self.hitbox = self.img.get_rect().inflate(0, 0)

    def bu_work(self):
        self.game.towerManager.delete_tower(self.tower)


class UpgradeButton(Button):
    def __init__(self, game, tower, num: int = 0):
        self.game = game
        self.type = tower.towerType
        self.num = num
        self.pos = (tower.hitbox.left-int(UP_WIDTH/2),
                    tower.hitbox.top+UP_WIDTH*num)
        self.screen = game.screen
        self.ifLiving = True
        self.et_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos
        self.tower = tower

    def et_set(self):
        temptImg = self.game.res.get_img(
            towers.towerUpgradeIndex[self.type][self.num])
        self.img = pygame.transform.scale(temptImg, (UP_WIDTH, UP_WIDTH))
        self.hitbox = self.img.get_rect().inflate(0, 0)

    def bu_work(self):
        self.game.towerManager.upgrade_tower(self.tower, self.num)


class BuManager():
    def __init__(self, game):
        self.game = game
        self.buttonList = []

    def check_bu_list(self, pos: tuple):
        for button in self.buttonList:
            if button.bu_check(pos):
                button.bu_work()
                return True
        return False

    def blit_bu_list(self):
        for button in self.buttonList:
            button.et_blit()

    def clear_bu_list(self):
        self.buttonList.clear()
