import pygame
import entities
import friends
from math import dist
from constants import *
from numpy import arctan2
towerUpgradeIndex = {TO_BASE: [TO_TEST, TO_CANNON, TO_ARCHER, TO_WIZARD]}


class ToManager:
    def __init__(self, game):
        self.towerList = []
        self.operateButtonManager = entities.BuManager(game)
        self.towerNum = 0
        self.game = game
        self.ifOperating = False
        self.selectedTower = None
        self.numBases = len(game.map.towerBaseList)
        for pos in game.map.towerBaseList:
            self.towerList.append(Base(pos, self.game))

    def create_tower(self, pos: tuple, type: int):
        if type == TO_ARCHER:
            self.towerList.append(ArcherTower(pos, self.game))
        if type == TO_CANNON:
            self.towerList.append(CannonTower(pos, self.game))
        if type == TO_WIZARD:
            self.towerList.append(WizardTower(pos, self.game))
        # test
        if type == TO_TEST:
            self.towerList.append(TestTower(pos, self.game))
        print(f"tower at:{str(pos)} starts working")
        self.towerNum += 1

    def search_tower(self, pos: tuple, mode=COMMON):
        if mode == COMMON:
            for tower in self.towerList:
                if tower.ifWorking and tower.hitbox.collidepoint(pos):
                    return tower
            return False
        elif mode == UPGRADE:
            for tower in self.towerList:
                if tower.ifSelected and tower.hitbox.collidepoint(pos):
                    return tower
            return False

    def select_tower(self, pos: tuple):
        tower = self.search_tower(pos)
        if tower == False:
            pass
        else:
            print('Operating')
            self.ifOperating = True
            self.selectedTower = tower
            tower.ifSelected = True

    def create_operateButtons(self):
        if self.selectedTower.ifUpgradeable:
            for num in range(len(towerUpgradeIndex[self.selectedTower.towerType])):
                self.operateButtonManager.buttonList.append(entities.UpgradeButton(self.game,
                                                                                   self.selectedTower,
                                                                                   num))
        if self.selectedTower.towerType != TO_BASE:
            self.operateButtonManager.buttonList.append(
                entities.TowerDeleteButton(self.game, self.selectedTower))

    def delete_tower(self, tower):
        tower.ifSelected = False
        tower.ifWorking = False
        tower.to_reset()
        basePos = tower.pos
        for t in self.towerList:  # set the base
            if t.towerType == TO_BASE and t.hitbox.collidepoint(basePos):
                t.ifWorking = True
                t.ifSelected = True
                self.selectedTower = t

    def upgrade_tower(self, tower, num: int):
        tower.ifSelected = False
        if not tower.towerType in towerUpgradeIndex:
            return
        tower.ifWorking = False  # stop old tower
        tower.to_reset()
        newTowerPos = tower.pos
        # set the new one
        self.create_tower(newTowerPos, towerUpgradeIndex[tower.towerType][num])
        self.selectedTower = self.towerList[-1]
        self.selectedTower.ifSelected = True

    def manage_to_list(self):
        temptList = self.towerList[:self.numBases]
        for tower in self.towerList[self.numBases:]:
            if tower.ifWorking:
                tower.to_search(self.game.enemyManager.enemyList)
                tower.to_prepare()
                if tower.ifReady and tower.ifFoundTarget:
                    tower.to_attack()
                temptList.append(tower)
        self.towerList = temptList

    def blit_to_list(self):
        for tower in self.towerList:
            if tower.ifWorking:
                tower.to_blit()

    def clear_to_list(self):
        self.towerList.clear()

    def quit_operatingmode(self):
        self.operateButtonManager.clear_bu_list()
        self.selectedTower.ifSelected = False
        self.ifOperating = False
        self.selectedTower = None

    def reset(self):
        self.clear_to_list()
        self.towerNum = 0


class Tower:
    def __init__(self, pos: tuple, game):
        # basic data
        self.game = game
        self.pos = pos
        self.ifWorking = True
        self.ifReady = False
        self.prepTimer = 0
        # select mode
        self.ifSelected = False
        # attack and search
        self.ifFoundTarget = False
        self.target = None
        # img
        self.screen = game.screen
        self.to_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos
        # upgrade
        self.ifUpgradeable = self.towerType in towerUpgradeIndex

    def to_set(self):
        # basic data
        self.prepInterval = TO_INTERVAL_D  # example
        self.ammo = None  # example
        self.searchRange = TO_RANGE_D  # example
        self.accuracy = 1  # example
        self.towerType = TO_TEST  # example
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-5, -5)  # example

    def to_prepare(self):
        if not self.ifReady:
            self.prepTimer += 1
            if self.prepTimer == self.prepInterval:
                self.ifReady = True
                self.prepTimer = 0

    def to_blit(self):
        self.screen.blit(self.img, self.img_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), self.hitbox, 1)
        if self.ifSelected:
            if self.ifFoundTarget:
                pygame.draw.line(self.screen, (0, 0, 255),
                                 self.pos, self.target.pos)
            pygame.draw.circle(self.screen, (0, 0, 255),
                               self.pos, self.searchRange, 1)

    def to_attack(self):
        routeIndex = self.target.routeIndex
        time = round(
            dist(self.pos, routeIndex[self.target.location])/AM_SPEED_ARROW)
        destLoc = self.target.location+time
        if destLoc > len(routeIndex):
            destLoc = len(routeIndex)
        self.game.ammoManager.create_ammo(
            self.pos, routeIndex[destLoc], self.ammo)
        self.ifReady = False

    def to_search(self, enemyList):
        self.ifFoundTarget = False
        for enemy in enemyList:
            dis = dist(self.pos, enemy.pos)
            if dis < self.searchRange:
                if self.ifFoundTarget:
                    if self.target.location > enemy.location:
                        pass
                    else:
                        self.target = enemy
                else:
                    self.target = enemy
                    self.ifFoundTarget = True

    def to_skill(self):
        pass

    def to_reset(self):
        self.ifReady = False
        self.prepTimer = 0
        self.ifSelected = False
        self.selTimer = 0
        self.dest = None


class Base(Tower):
    def to_set(self):
        # basic data
        self.prepInterval = TO_INTERVAL_D
        self.ammo = None
        self.towerType = TO_BASE
        self.searchRange = 0
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-5, -5)

    def to_search(self):
        pass

    def to_attack(self):
        pass


class TestTower(Tower):
    def to_set(self):
        # attack
        self.prepInterval = TO_INTERVAL_D
        self.ammo = AM_ARROW
        self.searchRange = TO_RANGE_D
        self.accuracy = 1
        self.towerType = TO_TEST
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-5, -5)


class ArcherTower(Tower):
    def to_set(self):
        # attack
        self.prepInterval = TO_INTERVAL_ARCHER
        self.ammo = AM_ARROW
        self.searchRange = TO_RANGE_ARCHER
        self.accuracy = 1
        self.towerType = TO_ARCHER
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-5, -5)


class CannonTower(Tower):
    def to_set(self):
        # attack
        self.prepInterval = TO_INTERVAL_CANNON
        self.ammo = AM_CANNONBALL
        self.searchRange = TO_RANGE_CANNON
        self.accuracy = 1
        self.towerType = TO_CANNON
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-5, -5)


class WizardTower(Tower):
    def to_set(self):
        # attack
        self.prepInterval = TO_INTERVAL_WIZARD
        self.ammo = AM_BEAM
        self.searchRange = TO_RANGE_WIZARD
        self.accuracy = 1
        self.towerType = TO_WIZARD
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-5, -5)
