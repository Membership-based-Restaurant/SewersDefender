import pygame
import os
import copy
import json
from constants import *


class MapCreate:
    def __init__(self):
        self.mapPath = 'maps/map_test.json'
        pygame.init()
        # img
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption('preview')
        self.screen.fill((181, 230, 29))
        self.bkPath = 'resources/bktest.png'
        # data
        temptList = []
        self.routeIndex = []  # routeIndex[routeNum][location]=(x,y)
        for x in range(1200):
            temptList.append((x, 400))
        self.routeIndex.append(copy.deepcopy(temptList))
        self.finishPosList = [(1200, 400)]  # [(x,y)]
        self.mapTackList = [[[60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            60, SUMMON_TE, 60, SUMMON_TE, 60, SUMMON_TE,
                            # mapTaskList[waveNum][routeNum][taskLoc]=task
                              WAVE_END]]]
        self.numEnemies = 48
        self.numRoutes = len(self.routeIndex)
        self.numWaves = len(self.mapTackList)
        self.towerBaseList = [(300, 350), (300, 450),
                              (600, 350), (600, 450), (900, 350), (900, 450)]
        self.draw_map()

    def get_info(self):
        print('routeIndex:', self.routeIndex)
        print('numRoutes:', self.numRoutes)
        print('finishPosList:', self.finishPosList)
        print('mapTaskList:', self.mapTackList)
        print('numEnemies:', self.numEnemies)
        print('numWaves:', self.numWaves)
        print('towerBaseList:', self.towerBaseList)
        print('self.bkPath:', self.bkPath)

    def draw_map(self):
        for routeNum in range(self.numRoutes):
            for location in self.routeIndex[routeNum]:
                pygame.draw.circle(self.screen, (173, 112, 63), location, 30)
        pygame.display.flip()
        self.img = self.screen.copy()

    def save_map(self):
        print('saving map')
        pygame.image.save(self.img, self.bkPath)
        mapInfoDict = {'routeIndex': self.routeIndex,
                       'numRoutes': self.numRoutes,
                       'finishPosList': self.finishPosList,
                       'mapTaskList': self.mapTackList,
                       'numEnemies': self.numEnemies,
                       'numWaves': self.numWaves,
                       'towerBaseList': self.towerBaseList,
                       'bkPath': self.bkPath}
        try:
            with open(self.mapPath, 'w', encoding='utf-8') as f:
                json.dump(mapInfoDict, f, indent=4)
                print('saved')
                return True
        except FileNotFoundError:
            print('fail to open map file')
            return False


if __name__ == '__main__':
    m = MapCreate()
    while True:
        ifQuit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ifQuit = True
                break
        if ifQuit:
            break
    m.get_info()
    os.system('pause')
    m.save_map()
