import pygame
import constants as c


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
        self.screen = game.screen
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
        self.img = self.game.res.get_img(c.EnemyType.TEST)  # example
        # basic data
        self.speed = c.EM_SPEED_D  # example
        self.hp = c.EM_HP_D  # example
        self.physicalDefence = c.EM_P_DEFENCE_D  # example
        self.magicalDefence = c.EM_M_DEFENCE_D  # example
        self.hitbox = self.img.get_rect().inflate(-5, -5)  # example
        self.reward = c.EM_REWARD_COMMON  # example
        # attack
        self.damage = c.EM_DAMAGE_D  # example

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
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.TEST)
        # basic data
        self.speed = c.EM_SPEED_D
        self.hp = c.EM_HP_D
        self.physicalDefence = c.EM_P_DEFENCE_D
        self.magicalDefence = c.EM_M_DEFENCE_D
        self.hitbox = self.img.get_rect().inflate(-10, -10)
        self.reward = c.EM_REWARD_COMMON
        # attack
        self.damage = c.EM_DAMAGE_D

    def en_skill(self):
        pass


class CommonEnemy(Enemy):
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.COMMON)
        # basic data
        self.speed = c.EM_SPEED_COMMON
        self.hp = c.EM_HP_COMMON
        self.physicalDefence = c.EM_P_DEFENCE_COMMON
        self.magicalDefence = c.EM_M_DEFENCE_COMMON
        self.hitbox = self.img.get_rect().inflate(-0, -0)
        self.reward = c.EM_REWARD_COMMON
        # attack
        self.damage = c.EM_DAMAGE_COMMON

    def en_skill(self):
        pass


class ArmoredEnemy(Enemy):
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.ARMORED)
        # basic data
        self.speed = c.EM_SPEED_ARMORED
        self.hp = c.EM_HP_ARMORED
        self.physicalDefence = c.EM_P_DEFENCE_ARMORED
        self.magicalDefence = c.EM_M_DEFENCE_ARMORED
        self.hitbox = self.img.get_rect().inflate(-0, -0)
        self.reward = c.EM_REWARD_ARMORED
        # attack
        self.damage = c.EM_DAMAGE_ARMORED

    def en_skill(self):
        pass


class RapidEnemy(Enemy):
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.RAPID)
        # basic data
        self.speed = c.EM_SPEED_RAPID
        self.hp = c.EM_HP_RAPID
        self.physicalDefence = c.EM_P_DEFENCE_RAPID
        self.magicalDefence = c.EM_M_DEFENCE_RAPID
        self.hitbox = self.img.get_rect().inflate(-0, -0)
        self.reward = c.EM_REWARD_RAPID
        # attack
        self.damage = c.EM_DAMAGE_RAPID

    def en_skill(self):
        pass


class BossEnemy(Enemy):
    def en_set(self):
        # img
        self.img = self.game.res.get_img(c.EnemyType.BOSS)
        # basic data
        self.speed = c.EM_SPEED_BOSS
        self.hp = c.EM_HP_BOSS
        self.physicalDefence = c.EM_P_DEFENCE_BOSS
        self.magicalDefence = c.EM_M_DEFENCE_BOSS
        self.hitbox = self.img.get_rect().inflate(-0, -0)
        self.reward = c.EM_REWARD_BOSS
        # attack
        self.damage = c.EM_DAMAGE_BOSS
        self.skillInterval = c.EM_INTERVAL_BOSS
        self.c_skillInterval = c.EM_INTERVAL_BOSS

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
