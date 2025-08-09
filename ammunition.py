import pygame
from constants import *
from numpy import arctan2
from numpy import pi
from numpy import log
from random import randint
from math import cos, sin, dist


class AmManage:
    def __init__(self, game):
        self.game = game
        self.ammoList = []

    def create_ammo(self, startPos: tuple, targetPos: tuple, type=AM_ARROW):
        if type == AM_ARROW:
            self.ammoList.append(Arrow(startPos, targetPos, self.game))
        elif type == AM_BEAM:
            self.ammoList.append(Beam(startPos, targetPos, self.game))
        elif type == AM_CANNONBALL:
            self.ammoList.append(Cannonball(startPos, targetPos, self.game))
        elif type == AM_BULLET:
            self.ammoList.append(Bullet(startPos, targetPos, self.game))

    def manage_am_list(self):
        temptList = []
        for ammo in self.ammoList:
            if dist(ammo.pos, ammo.targetPos) < ammo.speed:
                # print('hit')
                ammo.am_conclude()
            else:
                ammo.am_move()
                temptList.append(ammo)
        self.ammoList = temptList

    def blit_am_list(self):
        for ammo in self.ammoList:
            ammo.am_blit()

    def clear_am_list(self):
        self.ammoList.clear()

    def reset(self):
        self.clear_ammo_list()


class Ammo:
    def __init__(self, startPos: tuple, targetPos: tuple, game):
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect
        self.pos = startPos
        self.targetPos = targetPos
        self.am_set()
        self.am_set_angel()

    def am_set(self):
        self.img = self.game.res.get_img(AM_ARROW)  # example
        self.damage = AM_DAMAGE_D  # example
        self.speed = AM_SPEED_D  # example

    def am_set_angel(self):
        x = [self.targetPos[0] - self.pos[0]]
        y = [self.targetPos[1] - self.pos[1]]
        self.angel = arctan2(y, x)
        # print(self.angel)

    def am_move(self):
        x = self.pos[0] + cos(self.angel) * self.speed
        y = self.pos[1] + sin(self.angel) * self.speed
        self.pos = (x, y)

    def am_conclude(self):
        for enemy in self.game.enemyManager.enemyList:
            if enemy.hitbox.collidepoint(self.targetPos):
                damage = 0
                if self.damage > enemy.physicalDefence:
                    damage = self.damage - enemy.physicalDefence  # example
                else:
                    pass
                enemy.hp -= damage
                if damage >= 1:
                    self.game.messageManager.create_message(
                        f"-{str(damage)}",
                        (self.targetPos[0], self.targetPos[1] - randint(20, 30)),
                        self.get_word_size(damage),
                    )
                break

    def am_blit(self):
        rotatedImg = pygame.transform.rotate(self.img, -self.angel / pi * 180)
        rotatedImg_rect = rotatedImg.get_rect()
        rotatedImg_rect.center = self.pos
        self.screen.blit(rotatedImg, rotatedImg_rect)

    def get_word_size(self, num: int):
        return int(4 * log(8 * num))


class Arrow(Ammo):
    def am_set(self):
        self.img = self.game.res.get_img(AM_ARROW)
        self.damage = AM_DAMAGE_ARROW
        self.speed = AM_SPEED_ARROW


class Bullet(Ammo):
    def am_set(self):
        self.img = self.game.res.get_img(AM_BULLET)
        self.damage = AM_DAMAGE_BULLET
        self.speed = AM_SPEED_BULLET


class Beam(Ammo):
    def am_set(self):
        self.img = self.game.res.get_img(AM_BEAM)
        self.damage = AM_DAMAGE_BEAM
        self.speed = AM_SPEED_BEAM

    def am_conclude(self):
        for enemy in self.game.enemyManager.enemyList:
            if enemy.hitbox.collidepoint(self.targetPos):
                damage = 0
                if self.damage > enemy.magicalDefence:
                    damage = self.damage - enemy.magicalDefence
                else:
                    pass
                enemy.hp -= damage
                if damage >= 1:
                    self.game.messageManager.create_message(
                        f"-{str(damage)}",
                        (self.targetPos[0], self.targetPos[1] - randint(20, 30)),
                        self.get_word_size(damage),
                    )
                break


class Cannonball(Ammo):
    def am_set(self):
        self.img = self.game.res.get_img(AM_CANNONBALL)
        self.damage = AM_DAMAGE_CANNONBALL
        self.speed = AM_SPEED_CANNONBALL

    def am_conclude(self):
        for enemy in self.game.enemyManager.enemyList:
            if dist(enemy.pos, self.targetPos) < AM_RANGE_CANNONBALL:
                damage = 0
                if self.damage > enemy.physicalDefence:
                    damage = self.damage - enemy.physicalDefence
                else:
                    pass
                enemy.hp -= damage
                if damage >= 1:
                    self.game.messageManager.create_message(
                        f"-{str(damage)}",
                        (self.targetPos[0], self.targetPos[1] - randint(20, 30)),
                        self.get_word_size(damage),
                    )
