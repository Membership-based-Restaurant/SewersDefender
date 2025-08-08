import pygame
from constants import *


class EnManager:
    def __init__(self, game):
        self.enemyList = []
        self.enemyNum = 0
        self.enemyKilledNum = 0
        self.game = game

    def create_enemy(self, type: int, routeNum: int):
        # print('execute task:',type)
        if type == SUMMON_CE:
            self.enemyList.append(CommonEnemy(
                self.game, self.enemyNum, routeNum))
        elif type == SUMMON_AE:
            self.enemyList.append(ArmoredEnemy(
                self.game, self.enemyNum, routeNum))
        elif type == SUMMON_RE:
            self.enemyList.append(RapidEnemy(
                self.game, self.enemyNum, routeNum))
        # test
        elif type == SUMMON_TE:
            self.enemyList.append(
                TestEnemy(self.game, self.enemyNum, routeNum))
        else:
            return False
        self.enemyNum += 1
        return True

    def manage_en_list(self):
        temptList = []
        for enemy in self.enemyList:
            if enemy.hp <= 0:
                self.enemyKilledNum += 1
                pass
            else:
                if enemy.ifStuck == True:
                    enemy.en_attack()
                else:
                    enemy.en_move()
                temptList.append(enemy)
        self.enemyList = temptList

    def blit_en_list(self):
        for enemy in self.enemyList:
            enemy.en_blit()

    def clear_en_list(self):
        self.enemyList.clear()

    def reset(self):
        self.clear_en_list()
        self.enemyNum = 0
        self.enemyKilledNum = 0


class Enemy:
    def __init__(self, game, enemyNum: int, routeNum: int):
        # image
        self.screen = game.screen
        # basic data
        self.num = enemyNum
        # attack
        self.ifLiving = True
        self.ifStuck = False
        self.oppo = None
        # route
        self.location = 0
        self.routeIndex = game.map.routeIndex[routeNum]
        self.pos = self.routeIndex[self.location]
        self.en_set(game)
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.img_rect.center
        self.c_hp = self.hp

    def en_set(self, game):
        # img
        self.img = game.res.get_img(EM_TEST)  # example
        # basic data
        self.speed = EM_SPEED_D  # example
        self.hp = EM_HP_D  # example
        self.physicalDefence = EM_P_DEFENCE_D  # example
        self.magicalDefence = EM_M_DEFENCE_D  # example
        self.hitbox = self.img.get_rect().inflate(-5, -5)  # example
        # attack
        self.damage = EM_DAMAGE_D  # example

    def en_move(self, temptSpeed=0):
        # move the enemy
        if len(self.routeIndex)-1-self.location < self.speed:
            self.ifStuck = True
            return
        if temptSpeed == 0:
            speed = self.speed
        else:
            speed = temptSpeed
        self.location += speed
        self.pos = self.routeIndex[self.location]
        self.img_rect.center = self.pos
        self.hitbox.center = self.img_rect.center

    def en_blit(self):
        self.screen.blit(self.img, self.img_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), self.hitbox, 1)
        pygame.draw.rect(self.screen,
                         (255, 0, 0),
                         (self.hitbox.centerx-int(self.c_hp/2),
                          self.hitbox.centery+10,
                          self.c_hp,
                          3
                          ))
        pygame.draw.rect(self.screen,
                         (0, 255, 0),
                         (self.hitbox.centerx-int(self.c_hp/2),
                          self.hitbox.centery+10,
                          self.hp,
                          3
                          ))

    def en_attack(self):
        pass

    def en_skill(self):
        pass


class TestEnemy(Enemy):
    def en_set(self, game):
        # img
        self.img = game.res.get_img(EM_TEST)
        # basic data
        self.speed = EM_SPEED_D
        self.hp = EM_HP_D
        self.physicalDefence = EM_P_DEFENCE_D
        self.magicalDefence = EM_M_DEFENCE_D
        self.hitbox = self.img.get_rect().inflate(-10, -10)
        # attack
        self.damage = EM_DAMAGE_D


class CommonEnemy(Enemy):
    def en_set(self, game):
        # img
        self.img = game.res.get_img(EM_COMMON)
        # basic data
        self.speed = EM_SPEED_COMMON
        self.hp = EM_HP_COMMON
        self.physicalDefence = EM_P_DEFENCE_COMMON
        self.magicalDefence = EM_M_DEFENCE_COMMON
        self.hitbox = self.img.get_rect().inflate(-10, -10)
        # attack
        self.damage = EM_DAMAGE_COMMON


class ArmoredEnemy(Enemy):
    def en_set(self, game):
        # img
        self.img = game.res.get_img(EM_ARMORED)
        # basic data
        self.speed = EM_SPEED_ARMORED
        self.hp = EM_HP_ARMORED
        self.physicalDefence = EM_P_DEFENCE_ARMORED
        self.magicalDefence = EM_M_DEFENCE_ARMORED
        self.hitbox = self.img.get_rect().inflate(-10, -10)
        # attack
        self.damage = EM_DAMAGE_ARMORED


class RapidEnemy(Enemy):
    def en_set(self, game):
        # img
        self.img = game.res.get_img(EM_RAPID)
        # basic data
        self.speed = EM_SPEED_RSPID
        self.hp = EM_HP_RAPID
        self.physicalDefence = EM_P_DEFENCE_RAPID
        self.magicalDefence = EM_M_DEFENCE_RAPID
        self.hitbox = self.img.get_rect().inflate(-10, -10)
        # attack
        self.damage = EM_DAMAGE_RAPID
