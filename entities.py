import sys
import pygame
import towers
import constants as c
from typing import override


class Entity:
    def __init__(self, page, pos: tuple[int, int]):
        self.page = page
        self.screen = self.page.screen
        self.ifLiving = True
        self.pos = pos
        self.et_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos

    def et_set(self):
        self.img = self.page.res.get_img(c.EntityType.FINISH)  # example
        self.hitbox = self.img.get_rect().inflate(-5, -5)  # example

    def et_blit(self):
        self.screen.blit(self.img, self.img_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), self.hitbox, 1)


class Finish(Entity):
    @override
    def et_set(self):  # example
        self.img = self.page.res.get_img(c.EntityType.FINISH)  # example
        self.hitbox = self.img.get_rect().inflate(-10, -10)  # example


class FinManager:
    def __init__(self, game):
        self.game = game
        self.finishList: list[Finish] = []

    def create_finish(self, pos: tuple[int, int]) -> None:
        self.finishList.append(Finish(self.game, pos))

    def if_lose(self) -> bool:
        for finish in self.finishList:
            for enemy in self.game.enemyManager.enemyList:
                if finish.hitbox.collidepoint(enemy.pos):
                    return True
        return False

    def blit_fin_list(self):
        for finish in self.finishList:
            finish.et_blit()


class Message:
    def __init__(
        self,
        screen: pygame.Surface,
        info: str,
        pos: tuple,
        size: int,
        color=(255, 0, 0),
        remaingTime=c.ME_R_TIME_D,
    ):
        self.screen = screen
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", size)
        self.img = font.render(info, True, color)
        self.img_rect = self.img.get_rect()
        self.img_rect.center = pos
        self.remainingTime = remaingTime
        self.me_set()

    def me_set(self):
        pass

    def me_blit(self):
        self.screen.blit(self.img, self.img_rect)
        self.remainingTime -= 1


class MeManager:
    def __init__(self, game):
        self.game = game
        self.messageList = []

    def create_message(self, info: str, pos: tuple, size: int, color=(255, 0, 0)):
        self.messageList.append(Message(self.game.screen, info, pos, size, color))

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


class TaskStartButton(Button):
    @override
    def et_set(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        wordImg = font.render("Start", True, (239, 228, 176))
        self.img = pygame.Surface((wordImg.get_width() + 20, wordImg.get_height() + 10))
        self.img.fill((135, 75, 24))
        pygame.draw.rect(self.img, (239, 228, 176), self.img.get_rect(), 1)
        self.img.blit(wordImg, (10, 10))
        self.hitbox = self.img.get_rect().inflate(-5, -5)

    @override
    def bu_work(self):
        self.ifLiving = False
        self.page.ifExecuteTasks = True


class ExitButton(Button):
    @override
    def et_set(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        wordImg = font.render("Exit", True, (239, 228, 176))
        self.img = pygame.Surface((wordImg.get_width() + 20, wordImg.get_height() + 10))
        self.img.fill((135, 75, 24))
        pygame.draw.rect(self.img, (239, 228, 176), self.img.get_rect(), 1)
        self.img.blit(wordImg, (10, 5))
        self.hitbox = self.img.get_rect().inflate(-5, -5)

    @override
    def bu_work(self):
        pygame.quit()
        sys.exit()


class TowerDeleteButton(Button):
    def __init__(self, game, tower):
        self.game = game
        self.pos = (tower.hitbox.centerx, tower.hitbox.bottom + int(c.UP_WIDTH / 2))
        self.screen = game.screen
        self.ifLiving = True
        self.et_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos
        self.tower = tower
        self.type = tower.towerType

    @override
    def et_set(self):
        temptImg = self.game.res.get_img(c.ButtonType.TO_DELETE)
        self.img = pygame.transform.scale(temptImg, (c.UP_WIDTH, c.UP_WIDTH))
        self.hitbox = self.img.get_rect().inflate(0, 0)

    @override
    def bu_work(self):
        self.game.towerManager.delete_tower(self.tower)


class UpgradeButton(Button):
    def __init__(self, game, tower, num: int = 0):
        self.game = game
        self.type = tower.towerType
        self.num = num
        self.pos = (
            tower.hitbox.left - int(c.UP_WIDTH / 2),
            tower.hitbox.top + c.UP_WIDTH * num,
        )
        self.screen = game.screen
        self.ifLiving = True
        self.et_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos
        self.tower = tower

    @override
    def et_set(self):
        temptImg = self.game.res.get_img(towers.towerUpgradeIndex[self.type][self.num])
        self.img = pygame.transform.scale(
            temptImg.subsurface((pygame.Rect(0, 0, 50, 50))), (c.UP_WIDTH, c.UP_WIDTH)
        )
        self.hitbox = self.img.get_rect().inflate(0, 0)

    @override
    def bu_work(self):
        self.game.towerManager.upgrade_tower(self.tower, self.num)


class PageChangeButton(Button):
    def __init__(self, destPage, pos: tuple):
        self.pageManager = destPage.pageManager
        self.pos = pos
        self.screen = self.pageManager.screen
        self.ifLiving = True
        self.et_set()
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos
        self.destPage = destPage

    @override
    def et_set(self):
        pass

    @override
    def bu_work(self):
        self.pageManager.currentPage = self.destPage


class EnterButton(PageChangeButton):
    @override
    def et_set(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        wordImg = font.render("Game", True, (239, 228, 176))
        self.img = pygame.Surface((wordImg.get_width() + 20, wordImg.get_height() + 10))
        self.img.fill((135, 75, 24))
        pygame.draw.rect(self.img, (239, 228, 176), self.img.get_rect(), 1)
        self.img.blit(wordImg, (10, 5))
        self.hitbox = self.img.get_rect().inflate(-5, -5)


class GamePauseButton(PageChangeButton):
    @override
    def et_set(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        wordImg = font.render("Pause", True, (239, 228, 176))
        self.img = pygame.Surface((wordImg.get_width() + 20, wordImg.get_height() + 10))
        self.img.fill((135, 75, 24))
        pygame.draw.rect(self.img, (239, 228, 176), self.img.get_rect(), 1)
        self.img.blit(wordImg, (10, 5))
        self.hitbox = self.img.get_rect().inflate(-5, -5)


class GameRestartButton(PageChangeButton):
    @override
    def et_set(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        wordImg = font.render("Replay", True, (239, 228, 176))
        self.img = pygame.Surface((wordImg.get_width() + 20, wordImg.get_height() + 10))
        self.img.fill((135, 75, 24))
        pygame.draw.rect(self.img, (239, 228, 176), self.img.get_rect(), 1)
        self.img.blit(wordImg, (10, 5))
        self.hitbox = self.img.get_rect().inflate(-5, -5)

    @override
    def bu_work(self):
        self.destPage.set_game_resources()
        self.destPage.buttonManager.clear_bu_list()
        self.destPage.set_buttons()
        self.pageManager.currentPage = self.destPage


class GameContinueButton(PageChangeButton):
    @override
    def et_set(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        wordImg = font.render("Continue", True, (239, 228, 176))
        self.img = pygame.Surface((wordImg.get_width() + 20, wordImg.get_height() + 10))
        self.img.fill((135, 75, 24))
        pygame.draw.rect(self.img, (239, 228, 176), self.img.get_rect(), 1)
        self.img.blit(wordImg, (10, 5))
        self.hitbox = self.img.get_rect().inflate(-5, -5)


class BackButton(PageChangeButton):
    @override
    def et_set(self):
        font = pygame.font.Font("resources/FanwoodText-Regular.ttf", c.WORD_SIZE)
        wordImg = font.render("Back", True, (239, 228, 176))
        self.img = pygame.Surface((wordImg.get_width() + 20, wordImg.get_height() + 10))
        self.img.fill((135, 75, 24))
        pygame.draw.rect(self.img, (239, 228, 176), self.img.get_rect(), 1)
        self.img.blit(wordImg, (10, 5))
        self.hitbox = self.img.get_rect().inflate(-5, -5)


class MapChooseButton(PageChangeButton):
    def __init__(self, mapPath, destPage, pos: tuple):
        self.pageManager = destPage.pageManager
        self.pos = pos
        self.screen = self.pageManager.screen
        self.ifLiving = True
        temptImg = pygame.image.load(f"{mapPath}bk.png").convert_alpha()
        self.img = pygame.transform.scale(temptImg, (120, 80))
        self.hitbox = self.img.get_rect().inflate(-5, -5)
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.pos
        self.hitbox.center = self.pos
        self.destPage = destPage
        self.path = mapPath

    @override
    def et_set(self):
        pass

    @override
    def bu_work(self):
        self.destPage.mapPath = self.path
        self.destPage.set_game_resources()
        self.destPage.set_buttons()
        self.pageManager.currentPage = self.destPage


class BuManager:
    def __init__(self, page):
        self.page = page
        self.buttonList = []

    def check_bu_list(self, pos: tuple):
        for button in self.buttonList:
            if button.ifLiving and button.bu_check(pos):
                button.bu_work()
                return True
        return False

    def blit_bu_list(self):
        for button in self.buttonList:
            if button.ifLiving:
                button.et_blit()

    def clear_bu_list(self):
        self.buttonList.clear()
