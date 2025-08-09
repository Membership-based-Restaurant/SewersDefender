import pygame
import sys
from typing import Union
import constants as c


class ImgRes:
    def __init__(self):
        # game
        self.icon = pygame.image.load("resources/icon.png").convert_alpha()
        # enemy
        self.AEimg = pygame.image.load("resources/armoredEnemy.png").convert_alpha()
        self.CEimg = pygame.image.load("resources/commonEnemy.png").convert_alpha()
        self.REimg = pygame.image.load("resources/rapidEnemy.png").convert_alpha()
        self.BEimg = pygame.image.load("resources/bossEnemy.png").convert_alpha()
        # tower
        self.ATimg = pygame.image.load("resources/archerTower.png").convert_alpha()
        self.WTimg = pygame.image.load("resources/wizardTower.png").convert_alpha()
        self.GTimg = pygame.image.load("resources/cannonTower.png").convert_alpha()
        self.BTimg = pygame.image.load("resources/baseTower.png").convert_alpha()
        self.MTimg = pygame.image.load("resources/marksmanTower.png").convert_alpha()
        self.STimg = pygame.image.load("resources/sniperTower.png").convert_alpha()
        # test
        self.TEimg = pygame.image.load("resources/fy.png").convert_alpha()
        self.TTimg = pygame.image.load("resources/mr.png").convert_alpha()
        # entity
        self.FETimg = pygame.image.load("resources/finish.png").convert_alpha()
        self.DBUimg = pygame.image.load("resources/delete.png").convert_alpha()
        # ammo
        self.AAMimg = pygame.image.load("resources/arrow.png")
        self.BAMimg = pygame.image.load("resources/beam.png")
        self.CAMimg = pygame.image.load("resources/cannonball.png")
        self.BuAMimg = pygame.image.load("resources/bullet.png")
        # dict
        self.imgDict = {
            c.EnemyType.ARMORED: self.AEimg,
            c.EnemyType.COMMON: self.CEimg,
            c.EnemyType.RAPID: self.REimg,
            c.EnemyType.TEST: self.TEimg,
            c.EnemyType.BOSS: self.BEimg,
            c.TowerType.ARCHER: self.ATimg,
            c.TowerType.WIZARD: self.WTimg,
            c.TowerType.CANNON: self.GTimg,
            c.TowerType.TEST: self.TTimg,
            c.TowerType.BASE: self.BTimg,
            c.TowerType.SNIPER: self.STimg,
            c.TowerType.MARKSMAN: self.MTimg,
            c.EntityType.FINISH: self.FETimg,
            c.ButtonType.TO_DELETE: self.DBUimg,
            c.AmmoType.ARROW: self.AAMimg,
            c.AmmoType.BEAM: self.BAMimg,
            c.AmmoType.CANNONBALL: self.CAMimg,
            c.AmmoType.BULLET: self.BuAMimg,
        }

    def get_img(
        self,
        sprite_type: Union[
            c.EnemyType,
            c.TowerType,
            c.EntityType,
            c.ButtonType,
            c.AmmoType,
        ],
    ):
        return self.imgDict[sprite_type]


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    screen.fill((255, 255, 255))
    i = ImgRes()
    img = i.get_img(c.ButtonType.ENTER)
    screen.blit(img, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
