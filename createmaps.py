import pygame
import copy
import json
import constants as c


class MapCreate:
    def __init__(self):
        self.mapPath = "game_maps/map1/"
        pygame.init()
        # img
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("preview")
        self.screen.fill((109, 163, 22))
        self.bkPath = f"{self.mapPath}bk.png"
        # data
        temptList = []
        self.routeIndex = []  # routeIndex[routeNum][location]=(x,y)
        for x in range(1200):
            temptList.append((x, 400))
        self.routeIndex.append(copy.deepcopy(temptList))
        self.finishPosList = [(1175, 400)]  # [(x,y)]
        self.mapTackList = [
            [
                [
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.COMMON,
                    60,
                    c.SummonType.ARMORED,
                    60,
                    c.SummonType.ARMORED,
                    60,
                    c.SummonType.ARMORED,
                    300,
                    c.TaskEvent.END,
                ]
            ],
            [
                [
                    60,
                    c.SummonType.ARMORED,
                    60,
                    c.SummonType.ARMORED,
                    60,
                    c.SummonType.ARMORED,
                    60,
                    c.SummonType.ARMORED,
                    60,
                    c.SummonType.ARMORED,
                    60,
                    c.SummonType.ARMORED,
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    300,
                    c.TaskEvent.END,
                ]
            ],
            [
                [
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    60,
                    c.SummonType.RAPID,
                    300,
                    c.SummonType.BOSS,
                    300,
                    c.TaskEvent.END,
                ]
            ],
        ]
        # mapTaskList[waveNum][routeNum][taskLoc]=task
        self.numRoutes = len(self.routeIndex)
        self.numWaves = len(self.mapTackList)
        self.towerBaseList = [
            (300, 350),
            (300, 450),
            (600, 350),
            (600, 450),
            (900, 350),
            (900, 450),
        ]
        self.initialMoney = 500
        self.draw_map()

    def get_info(self):
        print("routeIndex:", self.routeIndex)
        print("numRoutes:", self.numRoutes)
        print("finishPosList:", self.finishPosList)
        print("mapTaskList:", self.mapTackList)
        print("numWaves:", self.numWaves)
        print("towerBaseList:", self.towerBaseList)
        print("initialMoney:", self.initialMoney)

    def draw_map(self):
        for routeNum in range(self.numRoutes):
            for location in self.routeIndex[routeNum]:
                pygame.draw.circle(self.screen, (105, 74, 25), location, 30)
            for location in self.routeIndex[routeNum]:
                pygame.draw.circle(self.screen, (135, 95, 32), location, 27)
        pygame.display.flip()
        self.img = self.screen.copy()

    def save_map(self):
        print("saving map")
        pygame.image.save(self.img, self.bkPath)
        mapInfoDict = {
            "routeIndex": self.routeIndex,
            "numRoutes": self.numRoutes,
            "finishPosList": self.finishPosList,
            "mapTaskList": self.mapTackList,
            "numWaves": self.numWaves,
            "towerBaseList": self.towerBaseList,
            "initialMoney": self.initialMoney,
        }
        try:
            with open(f"{self.mapPath}map.json", "w", encoding="utf-8") as f:
                json.dump(mapInfoDict, f, indent=4)
                print("saved")
                return True
        except FileNotFoundError:
            print("fail to open map file")
            return False


if __name__ == "__main__":
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
    input("paused, enter to continue")
    m.save_map()
