from __future__ import annotations

import pygame
import constants as c
from numpy import arctan2, pi, log
from random import randint
from math import cos, floor, sin, dist
from typing import override


class AmManage:
    def __init__(self, game):
        self.game = game
        self.ammoList: list[Ammo] = []

    def create_ammo(
        self,
        ammo_type: c.AmmoType,
        startPos: tuple[float, float],
        targetPos: tuple[float, float] = None,
        target=None,
    ) -> None:
        if ammo_type == c.AmmoType.ARROW:
            self.ammoList.append(Arrow(startPos, targetPos, self.game))
        elif ammo_type == c.AmmoType.BEAM:
            self.ammoList.append(Beam(startPos, targetPos, self.game))
        elif ammo_type == c.AmmoType.CANNONBALL:
            self.ammoList.append(Cannonball(startPos, targetPos, self.game))
        elif ammo_type == c.AmmoType.BULLET:
            self.ammoList.append(Bullet(startPos, targetPos, self.game))
        elif ammo_type == c.AmmoType.BIGCANNONBALL:
            self.ammoList.append(BigCannnonball(startPos, targetPos, self.game))
        elif ammo_type == c.AmmoType.MISSILE:
            self.ammoList.append(Missile(startPos, target, self.game))
        elif ammo_type == c.AmmoType.GRANDBEAM:
            self.ammoList.append(GrandBeam(startPos, targetPos, self.game))
        elif ammo_type == c.AmmoType.MAGICBALL:
            self.ammoList.append(MagicBall(startPos, targetPos, self.game))
        elif ammo_type == c.AmmoType.HOLYWATER:
            self.ammoList.append(HolyWater(startPos, targetPos, self.game))

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

    def clear_ammo_list(self) -> None:
        self.ammoList.clear()

    def reset(self) -> None:
        self.clear_ammo_list()


class Ammo:
    def __init__(self, startPos: tuple, targetPos: tuple, game):
        self.game = game
        self.screen: pygame.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect
        self.pos = startPos
        self.targetPos = targetPos
        self.am_set()
        self.am_set_angel()

    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.ARROW)  # example
        self.damage = c.AM_DAMAGE_D  # example
        self.speed = c.AM_SPEED_D  # example

    def am_set_angel(self):
        x = self.targetPos[0] - self.pos[0]
        y = self.targetPos[1] - self.pos[1]
        self.angel = float(arctan2(y, x))

    def am_move(self):
        x = self.pos[0] + cos(self.angel) * self.speed
        y = self.pos[1] + sin(self.angel) * self.speed
        self.pos = (x, y)

    def am_conclude(self):
        for enemy in self.game.enemyManager.enemyList:
            if enemy.hitbox.collidepoint(self.targetPos):
                reduction = 0.04 * (
                    enemy.armor - self.damage / (enemy.armorToughness / 4 + 2)
                )
                damage = floor(self.damage * (1 - reduction))
                if damage < 0:
                    damage = 0
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
        size = int(4 * log(8 * num))
        if size < 14:
            size = 14
        return size


class Arrow(Ammo):
    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.ARROW)
        self.damage = c.AM_DAMAGE_ARROW
        self.speed = c.AM_SPEED_ARROW


class Bullet(Ammo):
    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.BULLET)
        self.damage = c.AM_DAMAGE_BULLET
        self.speed = c.AM_SPEED_BULLET


class Beam(Ammo):
    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.BEAM)
        self.damage = c.AM_DAMAGE_BEAM
        self.speed = c.AM_SPEED_BEAM

    @override
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


class MagicBall(Ammo):
    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.MAGICBALL)
        self.damage = c.AM_DAMAGE_MAGICBALL
        self.speed = c.AM_SPEED_MAGICBALL

    @override
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
                self.game.buffManager.create_buff(
                    c.BuffType.TOXICOSIS, c.AM_BUFF_DURATION_MAGICBALL, enemy
                )
                break


class HolyWater(Ammo):
    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.HOLYWATER)
        self.damage = c.AM_DAMAGE_HOLYWATER
        self.speed = c.AM_SPEED_HOLYWATER

    @override
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
                self.game.buffManager.create_buff(
                    c.BuffType.ARMORREDUCE, c.AM_BUFF_DURATION_HOLYWATER, enemy
                )
                break


class GrandBeam(Ammo):
    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.GRANDBEAM)
        self.damage = c.AM_DAMAGE_GRANDBEAM
        self.speed = c.AM_SPEED_GRANDBEAM
        self.range = c.AM_RANGE_GRANDBEAM

    @override
    def am_conclude(self):
        for enemy in self.game.enemyManager.enemyList:
            if dist(enemy.pos, self.targetPos) < self.range:
                damage = 0
                if self.damage > enemy.magicalDefence:
                    damage = self.damage - enemy.magicalDefence
                else:
                    pass
                enemy.hp -= damage
                if damage >= 1:
                    self.game.messageManager.create_message(
                        f"-{str(damage)}",
                        (enemy.pos[0], enemy.pos[1] - randint(20, 30)),
                        self.get_word_size(damage),
                    )
                self.game.buffManager.create_buff(
                    c.BuffType.DIZZY, c.AM_BUFF_DURATION_GRAMDBEAM, enemy
                )


class Cannonball(Ammo):
    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.CANNONBALL)
        self.damage = c.AM_DAMAGE_CANNONBALL
        self.speed = c.AM_SPEED_CANNONBALL
        self.range = c.AM_RANGE_CANNONBALL

    @override
    def am_conclude(self):
        for enemy in self.game.enemyManager.enemyList:
            if dist(enemy.pos, self.targetPos) < self.range:
                reduction = 0.04 * (
                    enemy.armor - self.damage / (enemy.armorToughness / 4 + 2)
                )
                damage = floor(self.damage * (1 - reduction))
                if damage < 0:
                    damage = 0
                enemy.hp -= damage
                if damage >= 1:
                    self.game.messageManager.create_message(
                        f"-{str(damage)}",
                        (enemy.pos[0], enemy.pos[1] - randint(20, 30)),
                        self.get_word_size(damage),
                    )

    @override
    def am_blit(self):
        rotatedImg = pygame.transform.rotate(self.img, -self.angel / pi * 180)
        rotatedImg_rect = rotatedImg.get_rect()
        rotatedImg_rect.center = self.pos
        # pygame.draw.circle(self.screen, (255, 0, 0, 128), self.targetPos, self.range, 1)
        self.screen.blit(rotatedImg, rotatedImg_rect)


class BigCannnonball(Cannonball):
    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.CANNONBALL)
        self.damage = c.AM_DAMAGE_BIGCANNONBALL
        self.speed = c.AM_SPEED_BIGCANNONBALL
        self.range = c.AM_RANGE_BIGCANNONBALL


class Missile(Ammo):
    @override
    def __init__(self, startPos: tuple, target, game):
        self.game = game
        self.screen: pygame.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect
        self.pos = startPos
        self.target = target
        self.targetPos = self.target.pos
        self.am_set()
        self.angel = 3 / 2 * pi

    @override
    def am_set(self):
        self.img = self.game.res.get_img(c.AmmoType.MISSILE)
        self.damage = c.AM_DAMAGE_MISSILE
        self.speed = c.AM_SPEED_MISSILE
        self.range = c.TO_RANGE_LAUNCHER

    def am_new_angel(self):
        if (
            self.game.enemyManager.enemyList
            and self.target not in self.game.enemyManager.enemyList
        ):
            self.am_search()
        self.targetPos = self.target.pos
        x = self.targetPos[0] - self.pos[0]
        y = self.targetPos[1] - self.pos[1]
        newAngel = float(arctan2(y, x))
        if self.angel < 0:
            self.angel += 2 * pi
        if newAngel < 0:
            newAngel += 2 * pi
        if self.angel > 2 * pi:
            self.angel -= 2 * pi
        d = newAngel - self.angel
        if abs(d) <= pi / 12:
            self.angel += d
        else:
            self.angel += pi / 12

    def am_search(self):
        ifFoundTarget = False
        for enemy in self.game.enemyManager.enemyList:
            if ifFoundTarget:
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
                ifFoundTarget = True

    @override
    def am_move(self):
        self.am_new_angel()
        x = self.pos[0] + cos(self.angel) * self.speed
        y = self.pos[1] + sin(self.angel) * self.speed
        self.pos = (x, y)

    @override
    def am_conclude(self):
        for enemy in self.game.enemyManager.enemyList:
            if dist(enemy.pos, self.targetPos) < self.range:
                reduction = 0.04 * (
                    enemy.armor - self.damage / (enemy.armorToughness / 4 + 2)
                )
                damage = floor(self.damage * (1 - reduction))
                if damage < 0:
                    damage = 0
                enemy.hp -= damage
                if damage >= 1:
                    self.game.messageManager.create_message(
                        f"-{str(damage)}",
                        (enemy.pos[0], enemy.pos[1] - randint(20, 30)),
                        self.get_word_size(damage),
                    )
