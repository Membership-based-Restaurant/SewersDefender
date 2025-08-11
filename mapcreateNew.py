import os
import pygame
import copy
import json
import constants as c

r = 1
u = 2
l = 3
d = 4
s = 5
e = 6
b = 7


class MapCreate:
    def __init__(self):
        self.mapPath = "game_maps/map2/"
        self.initialMoney = 500
        # fmt:off
        temptMap = [
            [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, b, 0, 0, 0, 0, b, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, d, b, 0,
                0, 0, 0, b, 0, 0, 0, b, 0, 0, 0, 0, 0, b, 0, b, 0, 0, 0, 0, b, d, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0,
                0, 0, 0, b, 0, 0, 0, b, 0, 0, 0, 0, 0, b, 0, b, 0, 0, 0, 0, b, d, 0, 0,
                e, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, b, 0,
                0, 0, 0, 0, 0, 0, b, 0, 0, 0, 0, b, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            ],
            [
                0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, r, r, r, r, r, r, r, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, d, l, l, l, l, l, l, l, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, e, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            ],
        ]
        # fmt:on
        startPosList = [
            (1, 3),
            (8, 1),
        ]  # finishPosList = [(1, 12), (8, 14)]  # [(x,y)]
        # fmt:off
        self.mapTaskList = [
            [
                [
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,60,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,60,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,60,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,60,
                    c.TaskEvent.END
                ],
                [
                    600,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,60,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,120,
                    c.SummonType.RAPID,120,c.SummonType.RAPID,120,c.SummonType.RAPID,120,
                    c.TaskEvent.END
                ],
            ],
            [
                [
                    600,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,60,
                    c.SummonType.RAPID,120,c.SummonType.RAPID,120,c.SummonType.RAPID,120,
                    c.SummonType.ARMORED,60,c.SummonType.COMMON,60,c.SummonType.ARMORED,60,
                    c.SummonType.ARMORED,60,c.SummonType.COMMON,60,c.SummonType.ARMORED,60,
                    c.SummonType.ARMORED,60,c.SummonType.COMMON,60,c.SummonType.ARMORED,60,
                    c.TaskEvent.END
                ],
                [
                    1200,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,60,
                    c.SummonType.RAPID,120,c.SummonType.RAPID,120,c.SummonType.RAPID,120,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,120,
                    c.SummonType.RAPID,120,c.SummonType.RAPID,120,c.SummonType.RAPID,120,
                    c.TaskEvent.END
                ],
            ],
            [
                [
                    600,
                    c.SummonType.ARMORED,60,c.SummonType.ARMORED,60,c.SummonType.ARMORED,60,
                    c.SummonType.ARMORED,60,c.SummonType.ARMORED,60,c.SummonType.ARMORED,60,
                    c.SummonType.ARMORED,60,c.SummonType.ARMORED,60,c.SummonType.ARMORED,60,
                    c.SummonType.ARMORED,60,c.SummonType.ARMORED,60,c.SummonType.ARMORED,60,
                    c.SummonType.BOSS,60,c.SummonType.RAPID,60,c.SummonType.RAPID,150,
                    c.SummonType.BOSS,60,c.SummonType.RAPID,60,c.SummonType.RAPID,150,
                    c.TaskEvent.END
                ],
                [
                    600,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,60,
                    c.SummonType.RAPID,120,c.SummonType.RAPID,120,c.SummonType.RAPID,120,
                    c.SummonType.COMMON,60,c.SummonType.COMMON,60,c.SummonType.COMMON,120,
                    c.SummonType.RAPID,120,c.SummonType.RAPID,120,c.SummonType.RAPID,120,
                    c.TaskEvent.END
                ],
            ],
        ]# mapTaskList[waveNum][routeNum][taskLoc] = task
        #!remember to add an END at the end of each wave
        # fmt:on
        # *create routeindex and towerbaselist
        self.routeIndex = []
        self.towerBaseList = []
        self.finishPosList = []
        self.startPosList = []
        for route in temptMap:
            n = 0
            for poi in route:
                if poi == b:
                    x = n % 24
                    y = n // 24
                    self.towerBaseList.append(self.pos_convert((x, y)))
                n += 1
        for n in range(len(temptMap)):
            # get the start point
            route = temptMap[n]
            temptList = []
            currentPos = (startPosList[n][0] - 1, startPosList[n][1] - 1)
            self.startPosList.append(self.pos_convert(currentPos))
            temptList.append(self.pos_convert(currentPos))
            while True:
                # move
                flag = route[currentPos[0] + currentPos[1] * 24]
                if flag == r:
                    currentPos = (currentPos[0] + 1, currentPos[1])
                    for i in range(50):
                        temptList.append((temptList[-1][0] + 1, temptList[-1][1]))
                if flag == l:
                    currentPos = (currentPos[0] - 1, currentPos[1])
                    for i in range(50):
                        temptList.append((temptList[-1][0] - 1, temptList[-1][1]))
                if flag == u:
                    currentPos = (currentPos[0], currentPos[1] - 1)
                    for i in range(50):
                        temptList.append((temptList[-1][0], temptList[-1][1] - 1))
                if flag == d:
                    currentPos = (currentPos[0], currentPos[1] + 1)
                    for i in range(50):
                        temptList.append((temptList[-1][0], temptList[-1][1] + 1))
                if flag == e:
                    self.finishPosList.append(self.pos_convert(currentPos))
                    break
            self.routeIndex.append(temptList)
        self.numRoutes = len(self.routeIndex)
        self.numWaves = len(self.mapTaskList)
        self.mapInfoDict = {
            "routeIndex": self.routeIndex,
            "numRoutes": self.numRoutes,
            "finishPosList": self.finishPosList,
            "mapTaskList": self.mapTaskList,
            "numWaves": self.numWaves,
            "towerBaseList": self.towerBaseList,
            "initialMoney": self.initialMoney,
        }
        self.draw_map()

    def pos_convert(self, pos: tuple):
        return (pos[0] * 50 + 24, 100 + pos[1] * 50 + 24)

    def get_info(self):
        print(self.mapInfoDict)

    def draw_map(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("preview")
        self.screen.fill((109, 163, 22))
        self.bkPath = f"{self.mapPath}bk.png"
        for route in self.routeIndex:
            for location in route:
                pygame.draw.circle(self.screen, (135, 95, 32), location, 25)
        startImg = pygame.image.load("resources/start.png").convert_alpha()
        rect = startImg.get_rect()
        for pos in self.startPosList:
            rect.center = pos
            self.screen.blit(startImg, rect)
        pygame.display.flip()
        self.img = self.screen.copy()
        ifQuit = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    ifQuit = True
                    break
            if ifQuit:
                break

    def save_map(self):
        print("saving map")
        pygame.image.save(self.img, self.bkPath)

        try:
            with open(f"{self.mapPath}map.json", "w", encoding="utf-8") as f:
                json.dump(self.mapInfoDict, f, indent=4)
                print("saved")
                return True
        except FileNotFoundError:
            print("fail to open map file")
            return False


if __name__ == "__main__":
    m = MapCreate()
    # os.system("pause")
    # m.get_info()
    os.system("pause")
    m.save_map()
