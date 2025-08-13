from __future__ import annotations

import pygame
import entities
from math import dist
from typing import TYPE_CHECKING, override
import constants as c

if TYPE_CHECKING:
    from enemies import Enemy


towerUpgradeIndex = {
    c.TowerType.BASE: [c.TowerType.CANNON, c.TowerType.ARCHER, c.TowerType.WIZARD],
    c.TowerType.ARCHER: [c.TowerType.MARKSMAN, c.TowerType.SNIPER],
    c.TowerType.CANNON: [c.TowerType.BIGCANNON, c.TowerType.LAUNCHER],
    c.TowerType.WIZARD: [c.TowerType.ARCHMAGE, c.TowerType.WITCH, c.TowerType.PASTOR],
}
towerCostIndex = {
    c.TowerType.BASE: 0,
    c.TowerType.ARCHER: c.TO_COST_ARCHER,
    c.TowerType.CANNON: c.TO_COST_CANNON,
    c.TowerType.WIZARD: c.TO_COST_WIZARD,
    c.TowerType.SNIPER: c.TO_COST_SNIPER,
    c.TowerType.MARKSMAN: c.TO_COST_MARKSMAN,
    c.TowerType.BIGCANNON: c.TO_COST_BIGCANNON,
    c.TowerType.LAUNCHER: c.TO_COST_LAUNCHER,
    c.TowerType.ARCHMAGE: c.TO_COST_ARCHMAGE,
    c.TowerType.WITCH: c.TO_COST_WITCH,
    c.TowerType.PASTOR: c.TO_COST_PASTOR,
}


class ToManager:
    def __init__(self, game):
        self.towerList: list[Tower] = []
        self.operateButtonManager = entities.BuManager(game)
        self.towerNum = 0
        self.game = game
        self.ifOperating = False
        self.selectedTower: Tower | None = None
        self.numBases = len(game.map.towerBaseList)
        for pos in game.map.towerBaseList:
            self.towerList.append(Base(pos, self.game))

    def create_tower(self, pos: tuple, type: c.TowerType):
        if type == c.TowerType.ARCHER:
            self.towerList.append(ArcherTower(pos, self.game))
        elif type == c.TowerType.CANNON:
            self.towerList.append(CannonTower(pos, self.game))
        elif type == c.TowerType.WIZARD:
            self.towerList.append(WizardTower(pos, self.game))
        elif type == c.TowerType.MARKSMAN:
            self.towerList.append(MarksmanTower(pos, self.game))
        elif type == c.TowerType.SNIPER:
            self.towerList.append(SniperTower(pos, self.game))
        elif type == c.TowerType.BIGCANNON:
            self.towerList.append(BigCannonTower(pos, self.game))
        elif type == c.TowerType.LAUNCHER:
            self.towerList.append(LauncherTower(pos, self.game))
        elif type == c.TowerType.WITCH:
            self.towerList.append(WitchTower(pos, self.game))
        elif type == c.TowerType.ARCHMAGE:
            self.towerList.append(ArchmageTower(pos, self.game))
        elif type == c.TowerType.PASTOR:
            self.towerList.append(PastorTower(pos, self.game))
        # test
        """if type == c.TowerType.TEST:
            self.towerList.append(TestTower(pos, self.game))"""
        print(f"tower at:{str(pos)} starts working")
        self.game.map.money -= towerCostIndex[type]
        self.towerNum += 1

    def search_tower(self, pos: tuple, mode=c.COMMON):
        if mode == c.COMMON:
            for tower in self.towerList:
                if tower.ifLiving and tower.hitbox.collidepoint(pos):
                    return tower
            return False
        elif mode == c.UPGRADE:
            for tower in self.towerList:
                if tower.ifSelected and tower.hitbox.collidepoint(pos):
                    return tower
            return False

    def select_tower(self, pos: tuple):
        tower = self.search_tower(pos)
        if not tower:
            pass
        else:
            print("Operating")
            self.ifOperating = True
            self.selectedTower = tower
            tower.ifSelected = True

    def create_operateButtons(self) -> None:
        if not self.selectedTower:
            return
        if self.selectedTower.ifUpgradeable:
            for num in range(len(towerUpgradeIndex[self.selectedTower.towerType])):
                self.operateButtonManager.buttonList.append(
                    entities.UpgradeButton(self.game, self.selectedTower, num)
                )
        if self.selectedTower.towerType != c.TowerType.BASE:
            self.operateButtonManager.buttonList.append(
                entities.TowerDeleteButton(self.game, self.selectedTower)
            )

    def delete_tower(self, tower):
        tower.ifSelected = False
        tower.ifLiving = False
        tower.to_reset()
        basePos = tower.pos
        for t in self.towerList:  # set the base
            if t.towerType == c.TowerType.BASE and t.hitbox.collidepoint(basePos):
                t.ifLiving = True
                t.ifSelected = True
                self.selectedTower = t

    def upgrade_tower(self, tower, num: int):
        if tower.towerType not in towerUpgradeIndex:
            return
        if (
            towerCostIndex[towerUpgradeIndex[tower.towerType][num]]
            > self.game.map.money
        ):
            self.game.messageManager.create_message("Not enough money", tower.pos, 20)
            return
        tower.ifSelected = False
        tower.ifLiving = False  # stop old tower
        tower.to_reset()
        newTowerPos = tower.pos
        # set the new one
        self.create_tower(newTowerPos, towerUpgradeIndex[tower.towerType][num])
        self.selectedTower = self.towerList[-1]
        self.selectedTower.ifSelected = True

    def manage_to_list(self):
        temptList = self.towerList[: self.numBases]
        for tower in self.towerList[self.numBases :]:
            if tower.ifLiving:
                tower.to_search(self.game.enemyManager.enemyList)
                tower.to_prepare()
                if tower.ifReady and tower.ifFoundTarget:
                    tower.to_attack()
                temptList.append(tower)
        self.towerList = temptList

    def blit_to_list(self):
        for tower in self.towerList:
            if tower.ifLiving:
                tower.to_blit()

    def clear_to_list(self):
        self.towerList.clear()

    def quit_operatingmode(self) -> None:
        self.operateButtonManager.clear_bu_list()
        if self.selectedTower:
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
        self.ifLiving = True
        self.ifReady = False
        self.prepTimer = 0
        # select mode
        self.ifSelected = False
        # attack and search
        self.ifFoundTarget = False
        self.target: Enemy | None = None
        # img
        self.screen = game.screen
        self.to_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = (
            self.pos[0],
            self.pos[1] - int(0.15 * self.img_rect.height),
        )
        # upgrade
        self.ifUpgradeable = self.towerType in towerUpgradeIndex

    def to_set(self):
        # basic data
        self.prepInterval = c.TO_INTERVAL_D  # example
        self.ammo = None  # example
        self.searchRange = c.TO_RANGE_D  # example
        self.accuracy = 1  # example
        self.towerType = c.TowerType.TEST  # example
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-5, -20)  # example

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
            if self.ifFoundTarget and self.target is not None:
                pygame.draw.line(
                    self.screen, (200, 200, 200), self.pos, self.target.pos
                )
            pygame.draw.circle(self.screen, (0, 0, 255), self.pos, self.searchRange, 1)

    def to_attack(self) -> None:
        if self.target is None:
            return
        routeIndex = self.target.routeIndex
        time = round(
            dist(self.pos, routeIndex[self.target.location]) / c.AM_SPEED_ARROW
        )
        destLoc = self.target.location + time * self.target.speed
        if destLoc >= len(routeIndex):
            destLoc = len(routeIndex) - 1
        self.game.ammoManager.create_ammo(self.ammo, self.pos, routeIndex[destLoc])
        self.ifReady = False

    def to_search(self, enemyList: list[Enemy]) -> None:
        self.ifFoundTarget = False
        for enemy in enemyList:
            dis = dist(self.pos, enemy.pos)
            if dis < self.searchRange:
                if self.ifFoundTarget:
                    if (
                        self.target is not None
                        and len(self.target.routeIndex) - self.target.location
                        < len(enemy.routeIndex) - enemy.location
                    ):
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
    @override
    def to_set(self) -> None:
        # basic data
        self.prepInterval = c.TO_INTERVAL_D
        self.ammo = None
        self.towerType = c.TowerType.BASE
        self.searchRange = 0
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(0, -30)

    @override
    def to_search(self, enemyList: list[Enemy]) -> None:
        pass

    @override
    def to_attack(self) -> None:
        pass


class TestTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_D
        self.ammo = c.AmmoType.ARROW
        self.searchRange = c.TO_RANGE_D
        self.accuracy = 1
        self.towerType = c.TowerType.TEST
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-5, -5)


class ArcherTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_ARCHER
        self.ammo = c.AmmoType.ARROW
        self.searchRange = c.TO_RANGE_ARCHER
        self.accuracy = 1
        self.towerType = c.TowerType.ARCHER
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-0, -30)


class MarksmanTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_MARKSMAN
        self.ammo = c.AmmoType.ARROW
        self.searchRange = c.TO_RANGE_MARKSMAN
        self.accuracy = 1
        self.towerType = c.TowerType.MARKSMAN
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-0, -30)


class SniperTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_SNIPER
        self.ammo = c.AmmoType.BULLET
        self.searchRange = c.TO_RANGE_SNIPER
        self.accuracy = 1
        self.towerType = c.TowerType.SNIPER
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(-0, -30)

    @override
    def to_attack(self) -> None:
        if self.target is None:
            return
        routeIndex = self.target.routeIndex
        time = round(
            dist(self.pos, routeIndex[self.target.location]) / c.AM_SPEED_BULLET
        )
        destLoc = self.target.location + time * self.target.speed
        if destLoc >= len(routeIndex):
            destLoc = len(routeIndex) - 1
        self.game.ammoManager.create_ammo(self.ammo, self.pos, routeIndex[destLoc])
        self.ifReady = False


class CannonTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_CANNON
        self.ammo = c.AmmoType.CANNONBALL
        self.searchRange = c.TO_RANGE_CANNON
        self.accuracy = 1
        self.towerType = c.TowerType.CANNON
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(0, -30)

    @override
    def to_attack(self) -> None:
        if self.target is None:
            return
        routeIndex = self.target.routeIndex
        time = round(
            dist(self.pos, routeIndex[self.target.location]) / c.AM_SPEED_CANNONBALL
        )
        destLoc = self.target.location + time * self.target.speed
        if destLoc >= len(routeIndex):
            destLoc = len(routeIndex) - 1
        self.game.ammoManager.create_ammo(self.ammo, self.pos, routeIndex[destLoc])
        self.ifReady = False


class BigCannonTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_BIGCANNON
        self.ammo = c.AmmoType.BIGCANNONBALL
        self.searchRange = c.TO_RANGE_BIGCANNON
        self.accuracy = 1
        self.towerType = c.TowerType.BIGCANNON
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(0, -30)

    @override
    def to_attack(self) -> None:
        if self.target is None:
            return
        routeIndex = self.target.routeIndex
        time = round(
            dist(self.pos, routeIndex[self.target.location]) / c.AM_SPEED_BIGCANNONBALL
        )
        destLoc = self.target.location + time * self.target.speed
        if destLoc >= len(routeIndex):
            destLoc = len(routeIndex) - 1
        self.game.ammoManager.create_ammo(self.ammo, self.pos, routeIndex[destLoc])
        self.ifReady = False


class LauncherTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_LAUNCHER
        self.ammo = c.AmmoType.MISSILE
        self.searchRange = c.TO_RANGE_LAUNCHER
        self.accuracy = 1
        self.towerType = c.TowerType.LAUNCHER
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(0, -30)

    @override
    def to_attack(self) -> None:
        if self.target is None:
            return
        self.game.ammoManager.create_ammo(self.ammo, self.pos, target=self.target)
        self.ifReady = False


class WizardTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_WIZARD
        self.ammo = c.AmmoType.BEAM
        self.searchRange = c.TO_RANGE_WIZARD
        self.accuracy = 1
        self.towerType = c.TowerType.WIZARD
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(0, -30)

    @override
    def to_attack(self) -> None:
        if self.target is None:
            return
        routeIndex = self.target.routeIndex
        time = round(dist(self.pos, routeIndex[self.target.location]) / c.AM_SPEED_BEAM)
        destLoc = self.target.location + time * self.target.speed
        if destLoc >= len(routeIndex):
            destLoc = len(routeIndex) - 1
        self.game.ammoManager.create_ammo(self.ammo, self.pos, routeIndex[destLoc])
        self.ifReady = False


class WitchTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_WITCH
        self.ammo = c.AmmoType.MAGICBALL
        self.searchRange = c.TO_RANGE_WITCH
        self.accuracy = 1
        self.towerType = c.TowerType.WITCH
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(0, -30)

    @override
    def to_attack(self) -> None:
        if self.target is None:
            return
        routeIndex = self.target.routeIndex
        time = round(
            dist(self.pos, routeIndex[self.target.location]) / c.AM_SPEED_MAGICBALL
        )
        destLoc = self.target.location + time * self.target.speed
        if destLoc >= len(routeIndex):
            destLoc = len(routeIndex) - 1
        self.game.ammoManager.create_ammo(self.ammo, self.pos, routeIndex[destLoc])
        self.ifReady = False


class PastorTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_PASTOR
        self.ammo = c.AmmoType.HOLYWATER
        self.searchRange = c.TO_RANGE_PASTOR
        self.accuracy = 1
        self.towerType = c.TowerType.PASTOR
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(0, -30)

    @override
    def to_attack(self) -> None:
        if self.target is None:
            return
        routeIndex = self.target.routeIndex
        time = round(
            dist(self.pos, routeIndex[self.target.location]) / c.AM_SPEED_HOLYWATER
        )
        destLoc = self.target.location + time * self.target.speed
        if destLoc >= len(routeIndex):
            destLoc = len(routeIndex) - 1
        self.game.ammoManager.create_ammo(self.ammo, self.pos, routeIndex[destLoc])
        self.ifReady = False


class ArchmageTower(Tower):
    @override
    def to_set(self) -> None:
        # attack
        self.prepInterval = c.TO_INTERVAL_ARCHMAGE
        self.ammo = c.AmmoType.GRANDBEAM
        self.searchRange = c.TO_RANGE_ARCHMAGE
        self.accuracy = 1
        self.towerType = c.TowerType.ARCHMAGE
        # img
        self.img = self.game.res.get_img(self.towerType)
        self.hitbox = self.img.get_rect().inflate(0, -30)

    @override
    def to_attack(self) -> None:
        if self.target is None:
            return
        routeIndex = self.target.routeIndex
        time = round(
            dist(self.pos, routeIndex[self.target.location]) / c.AM_SPEED_GRANDBEAM
        )
        destLoc = self.target.location + time * self.target.speed
        if destLoc >= len(routeIndex):
            destLoc = len(routeIndex) - 1
        self.game.ammoManager.create_ammo(self.ammo, self.pos, routeIndex[destLoc])
        self.ifReady = False
