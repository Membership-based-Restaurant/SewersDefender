import pygame
import constants as c
from random import randint
from math import log
from typing import override


class EnManager:
    def __init__(self, game):
        self.enemyList: list[Enemy] = []
        self.enemyNum = 0
        self.enemyKilledNum = 0
        self.game = game

    def create_enemy(self, summon_type: c.SummonType, routeNum: int) -> bool:
        if summon_type == c.SummonType.COMMON:
            self.enemyList.append(CommonEnemy(self.game, self.enemyNum, routeNum))
        elif summon_type == c.SummonType.ARMORED:
            self.enemyList.append(ArmoredEnemy(self.game, self.enemyNum, routeNum))
        elif summon_type == c.SummonType.RAPID:
            self.enemyList.append(RapidEnemy(self.game, self.enemyNum, routeNum))
        elif summon_type == c.SummonType.BOSS:
            self.enemyList.append(BossEnemy(self.game, self.enemyNum, routeNum))
            print(1)
        elif summon_type == c.SummonType.TEST:
            self.enemyList.append(TestEnemy(self.game, self.enemyNum, routeNum))
        else:
            return False
        self.enemyNum += 1
        return True

    def manage_en_list(self):
        temptList = []
        for enemy in self.enemyList:
            if enemy.hp <= 0:
                enemy.ifLiving = False
                self.game.map.money += enemy.reward
                self.enemyKilledNum += 1
                pass
            else:
                if enemy.ifStuck:
                    enemy.en_attack()
                else:
                    enemy.en_move()
                enemy.en_skill()
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
        self.screen: pygame.Surface = game.screen
        # basic data
        self.game = game
        self.num = enemyNum
        # attack
        self.ifLiving = True
        self.ifStuck = False
        self.oppo = None
        # route
        self.location = 0
        self.routeIndex = game.map.routeIndex[routeNum]
        self.pos = self.routeIndex[self.location]
        self.en_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.img_rect.center
        self.c_hp = self.hp

    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.TEST)
        # basic data
        self.speed = c.EM_SPEED_D
        self.hp = c.EM_HP_D
        self.armor = c.EM_ARMOR_D
        self.armorToughness = c.EM_ARMOR_TOUGHNESS_D
        self.magicalDefence = c.EM_M_DEFENCE_D
        self.hitbox = self.img.get_rect().inflate(-5, -5)
        self.reward = c.EM_REWARD_COMMON
        # attack
        self.damage = c.EM_DAMAGE_D

    def en_move(self, temptSpeed=0):
        # move the enemy
        if len(self.routeIndex) - 1 - self.location < self.speed:
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
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (
                self.hitbox.centerx - int(self.c_hp / 2 * c.EM_HP_COEF),
                self.hitbox.centery + 10,
                int(self.c_hp * c.EM_HP_COEF),
                3,
            ),
        )
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            (
                self.hitbox.centerx - int(self.c_hp / 2 * c.EM_HP_COEF),
                self.hitbox.centery + 10,
                int(self.hp * c.EM_HP_COEF),
                3,
            ),
        )

    def en_attack(self):
        pass

    def en_skill(self):
        pass


class TestEnemy(Enemy):
    @override
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.TEST)
        # basic data
        self.speed = c.EM_SPEED_D
        self.hp = c.EM_HP_D
        self.armor = c.EM_ARMOR_D
        self.armorToughness = c.EM_ARMOR_TOUGHNESS_D
        self.magicalDefence = c.EM_M_DEFENCE_D
        self.hitbox = self.img.get_rect().inflate(-10, -10)
        self.reward = c.EM_REWARD_COMMON
        # attack
        self.damage = c.EM_DAMAGE_D

    @override
    def en_skill(self):
        pass


class CommonEnemy(Enemy):
    @override
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.COMMON)
        # basic data
        self.speed = c.EM_SPEED_COMMON
        self.hp = c.EM_HP_COMMON
        self.armor = c.EM_ARMOR_COMMON
        self.armorToughness = c.EM_ARMOR_TOUGHNESS_COMMON
        self.magicalDefence = c.EM_M_DEFENCE_COMMON
        self.hitbox = self.img.get_rect().inflate(-0, -0)
        self.reward = c.EM_REWARD_COMMON
        # attack
        self.damage = c.EM_DAMAGE_COMMON

    @override
    def en_skill(self):
        pass


class ArmoredEnemy(Enemy):
    @override
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.ARMORED)
        # basic data
        self.speed = c.EM_SPEED_ARMORED
        self.hp = c.EM_HP_ARMORED
        self.armor = c.EM_ARMOR_ARMORED
        self.armorToughness = c.EM_ARMOR_TOUGHNESS_ARMORED
        self.magicalDefence = c.EM_M_DEFENCE_ARMORED
        self.hitbox = self.img.get_rect().inflate(-0, -0)
        self.reward = c.EM_REWARD_ARMORED
        # attack
        self.damage = c.EM_DAMAGE_ARMORED

    @override
    def en_skill(self):
        pass


class RapidEnemy(Enemy):
    @override
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.RAPID)
        # basic data
        self.speed = c.EM_SPEED_RAPID
        self.hp = c.EM_HP_RAPID
        self.armor = c.EM_ARMOR_RAPID
        self.armorToughness = c.EM_ARMOR_TOUGHNESS_RAPID
        self.magicalDefence = c.EM_M_DEFENCE_RAPID
        self.hitbox = self.img.get_rect().inflate(-0, -0)
        self.reward = c.EM_REWARD_RAPID
        # attack
        self.damage = c.EM_DAMAGE_RAPID

    @override
    def en_skill(self):
        pass


class BossEnemy(Enemy):
    @override
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.BOSS)
        # basic data
        self.speed = c.EM_SPEED_BOSS
        self.hp = c.EM_HP_BOSS
        self.armor = c.EM_ARMOR_BOSS
        self.armorToughness = c.EM_ARMOR_TOUGHNESS_BOSS
        self.magicalDefence = c.EM_M_DEFENCE_BOSS
        self.hitbox = self.img.get_rect().inflate(-0, -0)
        self.reward = c.EM_REWARD_BOSS
        # attack
        self.damage = c.EM_DAMAGE_BOSS
        self.skillInterval = c.EM_INTERVAL_BOSS
        self.c_skillInterval = c.EM_INTERVAL_BOSS

    @override
    def en_skill(self):
        if self.skillInterval > 0:
            self.skillInterval -= 1
        else:
            if self.c_hp - self.hp > c.EM_BOSS_RECOVER:
                self.hp += c.EM_BOSS_RECOVER
                self.skillInterval = self.c_skillInterval
                self.game.messageManager.create_message(
                    f"+{str(c.EM_BOSS_RECOVER)}", self.pos, 30, (0, 255, 0)
                )


class BuffManager:
    def __init__(self, game):
        self.buffList: list[Buff] = []
        self.towerBuffList: list[Buff] = []
        self.game = game

    def check_buff_list(self):  # prevent repeat
        temptList: list[Buff] = []
        length = len(self.buffList)
        for i in range(length):
            buff1 = self.buffList[i]
            flag = True
            for j in range(i + 1, length):
                buff2 = self.buffList[j]
                if (
                    type(buff1) == type(buff2)
                    and buff1.target == buff2.target
                    and buff2.duration >= buff1.duration
                ):
                    buff1.duration = buff2.duration
                    self.buffList[j] = buff1
                    flag = False
            if flag:
                temptList.append(buff1)
        self.buffList = temptList

    def create_buff(self, type: c.BuffType, duration: int, target: Enemy):
        if type == c.BuffType.TOXICOSIS:
            self.buffList.append(Toxicosis(self.game, duration, target))
        if type == c.BuffType.ARMORREDUCE:
            self.buffList.append(ArmorReduce(self.game, duration, target))
        if type == c.BuffType.DIZZY:
            self.buffList.append(Dizzy(self.game, duration, target))
        pass

    def manage_buff_list(self):
        self.check_buff_list()
        temptList: list[Buff] = []
        for buff in self.buffList:
            if buff.duration < 0:
                buff.buff_dissolve()
            elif not buff.target.ifLiving:
                pass
            else:
                buff.buff_work()
                temptList.append(buff)
        self.buffList = temptList

    def blit_buff_list(self):
        for buff in self.buffList:
            buff.buff_blit()


class Buff:
    def __init__(self, game, duration: int, target: Enemy):
        self.game = game
        self.screen: pygame.Surface = self.game.screen
        self.target = target
        self.duration = duration
        self.c_duration = duration
        self.pos = target.pos
        self.buff_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos

    def buff_set(self):  # example
        self.img = self.game.res.get_img(None)
        pass

    def buff_work(self):  # example
        self.pos = self.target.pos
        self.img_rect.center = self.pos
        self.duration -= 1
        pass

    def buff_dissolve(self):  # example
        pass

    def get_word_size(self, num: int):
        size = int(4 * log(8 * num))
        if size < 14:
            size = 14
        return size

    def buff_blit(self):
        self.screen.blit(self.img, self.img_rect)


class Toxicosis(Buff):
    @override
    def buff_set(self):
        self.img = self.game.res.get_img(c.BuffType.TOXICOSIS)
        self.interval = 30
        self.c_interval = self.interval
        self.damage = c.BUFF_DAMAGE_TOXICOSIS

    @override
    def buff_work(self):
        if self.interval == 0:
            self.interval = self.c_interval
            self.target.hp -= self.damage
            self.game.messageManager.create_message(
                f"-{str(self.damage)}",
                (self.target.pos[0], self.target.pos[1] - randint(20, 30)),
                self.get_word_size(self.damage),
            )
        self.interval -= 1
        self.pos = self.target.pos
        self.img_rect.center = self.pos
        self.duration -= 1


class ArmorReduce(Buff):
    @override
    def buff_set(self):
        self.img = self.game.res.get_img(c.BuffType.ARMORREDUCE)
        self.c_armor = self.target.armor
        self.target.armor = 0

    @override
    def buff_dissolve(self):
        self.target.armor = self.c_armor


class Dizzy(Buff):
    @override
    def buff_set(self):
        self.img = self.game.res.get_img(c.BuffType.DIZZY)
        self.c_speed = self.target.speed
        self.target.speed = round(self.c_speed * 0.2)

    @override
    def buff_dissolve(self):
        self.target.speed = self.c_speed
