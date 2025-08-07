import pygame
import sys
from constants import *


class ImgRes():
    def __init__(self):
        # game
        self.icon = pygame.image.load("resources/icon.png").convert_alpha()
        # enemy
        self.AEimg = pygame.image.load("resources/ae.png").convert_alpha()
        self.CEimg = pygame.image.load("resources/ce.png").convert_alpha()
        self.REimg = pygame.image.load("resources/re.png").convert_alpha()
        # tower
        self.ATimg = pygame.image.load("resources/at.png").convert_alpha()
        self.WTimg = pygame.image.load("resources/wt.png").convert_alpha()
        self.GTimg = pygame.image.load("resources/gt.png").convert_alpha()
        self.BTimg = pygame.image.load("resources/bt.png").convert_alpha()
        # test
        self.TEimg = pygame.image.load("resources/fy.png").convert_alpha()
        self.TTimg = pygame.image.load("resources/mr.png").convert_alpha()
        # entity
        self.FETimg = pygame.image.load("resources/finish.png").convert_alpha()
        self.DETimg = pygame.image.load("resources/delete.png").convert_alpha()
        # ammo
        self.AMimg = pygame.image.load("resources/arrow.png")
        # dict
        self.imgDict = {EM_ARMORED: self.AEimg,
                        EM_COMMON: self.CEimg,
                        EM_RAPID: self.REimg,
                        EM_TEST: self.TEimg,

                        TO_ARCHER: self.ATimg,
                        TO_WIZARD: self.WTimg,
                        TO_CANNON: self.GTimg,
                        TO_TEST: self.TTimg,
                        TO_BASE: self.BTimg,

                        ET_FINISH: self.FETimg,
                        BU_TO_DELETE: self.DETimg,
                        AM_ARROW: self.AMimg,
                        }

    def get_img(self, type: int):
        return self.imgDict[type]


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    screen.fill((255, 255, 255))
    i = ImgRes()
    img = i.get_img(TO_BASE)
    screen.blit(img, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
