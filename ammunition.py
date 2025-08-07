import pygame
import entities
from constants import *
from numpy import arctan2
from numpy import pi
from math import cos, sin, dist


class AmManage():
    def __init__(self, game):
        self.game = game
        self.ammoList = []

    def create_ammo(self, startPos: tuple, targetPos: tuple, type=AM_ARROW,):
        if type == AM_ARROW:
            self.ammoList.append(Arrow(startPos, targetPos, self.game))

    def manage_am_list(self):
        temptList = []
        for ammo in self.ammoList:
            if dist(ammo.pos, ammo.targetPos) < ammo.speed:
                # print('hit')
                for enemy in self.game.enemyManager.enemyList:
                    if enemy.hitbox.collidepoint(ammo.targetPos):
                        damage = 0
                        if ammo.damageType == MAGIC:
                            if ammo.damage > enemy.magicalDefence:
                                damage = ammo.damage-enemy.magicalDefence
                            else:
                                pass
                        elif ammo.damageType == PHIYICS:
                            if ammo.damage > enemy.physicalDefence:
                                damage = ammo.damage-enemy.physicalDefence
                            else:
                                pass
                        enemy.hp -= damage
                        self.game.messageManager.create_message(f'-{str(damage)}',
                                                                (enemy.pos[0]+enemy.speed,
                                                                 enemy.img_rect.top),
                                                                damage)
                        break
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


class Ammo():
    def __init__(self, startPos: tuple, targetPos: tuple, game):
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect
        self.pos = startPos
        self.targetPos = targetPos
        self.am_set()
        self.am_set_angel()

    def am_set(self):
        self.img = self.game.res.get_img(AM_ARROW)  # e
        self.damage = AM_DAMAGE_D  # e
        self.damageType = PHIYICS  # e
        self.speed = AM_SPEED_D  # e

    def am_set_angel(self):
        x = [self.targetPos[0]-self.pos[0]]
        y = [self.targetPos[1]-self.pos[1]]
        self.angel = arctan2(y, x)
        # print(self.angel)

    def am_move(self):
        x = self.pos[0]+cos(self.angel)*self.speed
        y = self.pos[1]+sin(self.angel)*self.speed
        self.pos = (x, y)

    def am_blit(self):
        rotatedImg = pygame.transform.rotate(self.img, -self.angel/pi*180)
        rotatedImg_rect = rotatedImg.get_rect()
        rotatedImg_rect.center = self.pos
        self.screen.blit(rotatedImg, rotatedImg_rect)


class Arrow(Ammo):
    def am_set(self):
        self.img = self.game.res.get_img(AM_ARROW)
        self.damage = AM_DAMAGE_ARROW
        self.damageType = PHIYICS
        self.speed = AM_SPEED_ARROW
